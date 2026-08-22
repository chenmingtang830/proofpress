import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { performance } from "node:perf_hooks";
import {
  PROJECT_ROOT,
  canonicalJson,
  parseStageOutput,
  prohibitedInventoryEntries,
  readJson,
  recursiveInventory,
  sha256,
  writeJson,
} from "./core.mjs";
import { loadManifest, realRunBlockers, verifyFrozenFiles } from "./manifest.mjs";
import { StageController } from "../controller/stage-controller.mjs";
import { auditInformationParity, createTestOnlyCarrier } from "../parity/information-parity.mjs";
import { runTestOnlyH4Verifier } from "../policies/test-verifier-h4.mjs";
import { scoreRecord } from "../scoring/score.mjs";
import { validateRunRecord } from "../schemas/validate.mjs";
import { createTestWorkerSession } from "./worker-session.mjs";

const CONDITIONS = Object.freeze(["C1_ORDINARY_PORTABLE", "C2_PROOFPRESS"]);
const FIXTURE_ROOT = path.join(PROJECT_ROOT, "bench/fixtures/h4-msa-escalation-candidate/test-double");
const PROHIBITED_NAMES = Object.freeze([
  ".git",
  ".proofpress",
  ".codex",
  ".agents",
  ".claude",
  "ledger",
  "session",
  "transcript",
  "conversation",
  "memory",
  "orchestrator",
]);

export async function runBenchmark(options) {
  const manifest = await loadManifest(options.manifest);
  const frozen = await verifyFrozenFiles(manifest);
  if (!frozen.valid) throw new Error(`Frozen file mismatch: ${JSON.stringify(frozen.mismatches)}`);

  const testOnly = options.testOnly === true;
  if (!testOnly || options.adapter !== "deterministic-test") {
    const blockers = realRunBlockers(manifest);
    throw new Error(`Real execution blocked by unresolved freeze gates: ${blockers.join(", ")}`);
  }
  const pairedReplicates = Number(options.pairedReplicates ?? 1);
  if (pairedReplicates !== 1) throw new Error("This smallest H4 calibration permits exactly one TEST-ONLY paired replicate");
  const outputDirectory = path.resolve(options.output);
  enforceOutputBoundary(outputDirectory);
  await ensureOutputDirectory(outputDirectory);

  const invocationId = `TEST-ONLY-H4-${new Date().toISOString().replace(/[-:.]/g, "")}-${sha256(`${process.pid}-${Date.now()}-${Math.random()}`).slice(0, 10)}`;
  const commonInstruction = await fs.readFile(path.join(FIXTURE_ROOT, "common-instruction.md"));
  const schedule = manifest.horizon.stage_schedule;
  const invocationRoot = await fs.mkdtemp(path.join(os.tmpdir(), "relaybench-h4-"));
  const startedAt = new Date().toISOString();
  let preBoundary;
  let completed;
  try {
    preBoundary = Object.fromEntries(await Promise.all(CONDITIONS.map(async (condition) => [
      condition,
      await runPreBoundary({ condition, schedule, invocationRoot, commonInstruction }),
    ])));

    const parity = auditInformationParity(
      preBoundary.C1_ORDINARY_PORTABLE.transferPackage,
      preBoundary.C2_PROOFPRESS.transferPackage,
    );
    if (!parity.passed) throw new Error(`C1/C2 information parity failed: ${parity.errors.join("; ")}`);

    const verifier = await runTestOnlyH4Verifier({
      c1Files: preBoundary.C1_ORDINARY_PORTABLE.transferPackage,
      c2Files: preBoundary.C2_PROOFPRESS.transferPackage,
    });
    if (verifier.status !== "ok" || verifier.malformed) throw new Error("TEST-ONLY C2 verifier failed before receiver action");

    completed = Object.fromEntries(await Promise.all(CONDITIONS.map(async (condition) => [
      condition,
      await runPostBoundary({
        condition,
        invocationId,
        invocationRoot,
        pre: preBoundary[condition],
        parity,
        verifier: condition === "C2_PROOFPRESS" ? verifier : unavailableVerifier(),
        schedule,
      }),
    ])));
  } finally {
    await fs.rm(invocationRoot, { recursive: true, force: true });
  }

  const records = [];
  for (const condition of CONDITIONS) {
    const episode = completed[condition];
    const record = buildEpisodeRecord({ manifest, invocationId, condition, parity: episode.parity, episode });
    record.deterministic_score = scoreRecord(record);
    const validation = validateRunRecord(record);
    if (!validation.valid) throw new Error(`Run record schema violation: ${validation.errors.join("; ")}`);
    await writeJson(path.join(outputDirectory, record.result_file), record);
    records.push(record);
  }

  const runSet = {
    schema_version: 2,
    record_type: "h4_calibration_run_set",
    invocation_id: invocationId,
    test_only: true,
    publishable: false,
    generated_at: new Date().toISOString(),
    started_at: startedAt,
    horizon: "H4",
    stress_track: "EVOLVING_NEGOTIATION_STATE",
    conditions: CONDITIONS,
    paired_replicates: 1,
    episodes: records.length,
    stage_records: records.reduce((sum, record) => sum + record.stages.length, 0),
    cold_boundaries: records.reduce((sum, record) => sum + record.workspace_boundaries.length, 0),
    record_files: records.map((record) => record.result_file),
    note: "TEST-ONLY mechanics calibration. Excluded from benchmark metrics and never a benchmark result.",
  };
  await writeJson(path.join(outputDirectory, "TEST-ONLY-h4-run-set.json"), runSet);
  return { runSet, records };
}

async function runPreBoundary({ condition, schedule, invocationRoot, commonInstruction }) {
  const controller = new StageController(schedule);
  const workspace = await fs.mkdtemp(path.join(invocationRoot, `${condition}-sender-`));
  const initialInventory = await recursiveInventory(workspace);
  if (initialInventory.length) throw new Error("Sender session workspace was not created empty");
  await writeWorkspaceFile(workspace, "instructions/common.md", commonInstruction);
  const worker = createTestWorkerSession(workspace);
  const sessionToken = `${condition}-worker-${worker.pid}`;
  const stages = [];
  stages.push(await executeStage({ condition, controller, worker, workspace, sessionToken, scheduleIndex: 0 }));
  stages.push(await executeStage({ condition, controller, worker, workspace, sessionToken, scheduleIndex: 1 }));
  const senderExit = await worker.close();
  if (senderExit.code !== 0) throw new Error(`Sender TEST-ONLY worker failed: ${senderExit.stderr}`);

  const handoffState = Buffer.from(`${JSON.stringify({
    schema_version: 1,
    test_only: true,
    through_stage: "S2",
    readable_state: stages.at(-1).receiver_output.work_product,
    note: "Same readable handoff state in C1 and C2; not a legal conclusion.",
  }, null, 2)}\n`);
  await writeWorkspaceFile(workspace, "handoff-state.json", handoffState);
  const substantive = await readPackage(workspace);
  const transferPackage = condition === "C2_PROOFPRESS"
    ? [...substantive, { path: "proofpress/portable-carrier.test-only.json", content: createTestOnlyCarrier(substantive) }]
    : substantive;
  return {
    controller,
    workspace,
    worker_pid: worker.pid,
    worker_environment_keys: worker.environment_keys,
    sender_exit: senderExit,
    stages,
    transferPackage,
  };
}

async function runPostBoundary({ condition, invocationId, invocationRoot, pre, parity, verifier, schedule }) {
  const receiverWorkspace = await fs.mkdtemp(path.join(invocationRoot, `${condition}-receiver-`));
  const preTransferInventory = await recursiveInventory(receiverWorkspace);
  const previousGitAbsent = !await exists(path.join(receiverWorkspace, ".git"));
  await copyPackage(pre.transferPackage, receiverWorkspace);
  const postTransferInventory = await recursiveInventory(receiverWorkspace);
  const prohibited = prohibitedInventoryEntries(postTransferInventory, PROHIBITED_NAMES);
  const expectedFiles = pre.transferPackage.map((file) => file.path).sort();
  const actualFiles = postTransferInventory.filter((item) => item.type === "file").map((item) => item.path).sort();
  const onlyDeclared = canonicalJson(expectedFiles) === canonicalJson(actualFiles);
  const noLinks = postTransferInventory.every((item) => ["file", "directory"].includes(item.type));

  const senderWorkspace = pre.workspace;
  await fs.rm(senderWorkspace, { recursive: true, force: true });
  const senderWorkspaceRemoved = !await exists(senderWorkspace);
  const receiver = createTestWorkerSession(receiverWorkspace);
  const workerPidChanged = receiver.pid !== pre.worker_pid;
  const boundary = {
    boundary_id: `${invocationId}-${condition}-B1`,
    before_stage: "S3",
    valid: false,
    sender_worker_pid: pre.worker_pid,
    receiver_worker_pid: receiver.pid,
    worker_pid_changed: workerPidChanged,
    sender_worker_exited: pre.sender_exit.code === 0,
    sender_workspace_removed: senderWorkspaceRemoved,
    receiver_workspace_id: path.basename(receiverWorkspace),
    receiver_workspace_created_fresh: true,
    pre_transfer_inventory_empty: preTransferInventory.length === 0,
    pre_transfer_inventory: preTransferInventory,
    post_transfer_inventory: postTransferInventory,
    transferred_file_manifest: postTransferInventory.filter((item) => item.type === "file").map((item) => ({
      path: item.path,
      bytes: item.bytes,
      sha256: item.sha256,
      source: `sender-declared-package/${item.path}`,
      destination: `fresh-receiver/${item.path}`,
    })),
    declared_transfer_paths: expectedFiles,
    only_declared_transfer_package: onlyDeclared,
    previous_git_absent: previousGitAbsent,
    sender_ledger_absent: !postTransferInventory.some((item) => item.path === ".proofpress" || item.path.startsWith(".proofpress/")),
    session_state_absent: prohibited.length === 0,
    transcript_absent: prohibited.length === 0,
    conversation_absent: prohibited.length === 0,
    hidden_memory_absent: prohibited.length === 0,
    orchestrator_state_absent: prohibited.length === 0,
    prohibited_names_checked: PROHIBITED_NAMES,
    prohibited_entries_found: prohibited,
    no_links_or_special_files: noLinks,
    receiver_environment_keys: receiver.environment_keys,
  };
  boundary.valid = Boolean(
    boundary.worker_pid_changed && boundary.sender_worker_exited && boundary.sender_workspace_removed &&
    boundary.pre_transfer_inventory_empty && boundary.only_declared_transfer_package && boundary.previous_git_absent &&
    boundary.sender_ledger_absent && boundary.session_state_absent && boundary.transcript_absent &&
    boundary.conversation_absent && boundary.hidden_memory_absent && boundary.orchestrator_state_absent && boundary.no_links_or_special_files,
  );
  if (!boundary.valid) {
    await receiver.close();
    throw new Error(`Cold boundary failed for ${condition}`);
  }

  const sessionToken = `${condition}-worker-${receiver.pid}`;
  const stages = [...pre.stages];
  stages.push(await executeStage({
    condition,
    controller: pre.controller,
    worker: receiver,
    workspace: receiverWorkspace,
    sessionToken,
    scheduleIndex: 2,
    boundaryEvidence: boundary,
    verifierEvidence: verifier,
  }));
  stages.push(await executeStage({
    condition,
    controller: pre.controller,
    worker: receiver,
    workspace: receiverWorkspace,
    sessionToken,
    scheduleIndex: 3,
  }));
  const receiverExit = await receiver.close();
  if (receiverExit.code !== 0) throw new Error(`Receiver TEST-ONLY worker failed: ${receiverExit.stderr}`);
  if (!pre.controller.state.complete) throw new Error("Stage controller did not complete H4");
  return {
    condition,
    stages,
    stage_controller: pre.controller.state,
    parity,
    verifier,
    boundary,
    receiver_exit: receiverExit,
  };
}

async function executeStage({
  condition,
  controller,
  worker,
  workspace,
  sessionToken,
  scheduleIndex,
  boundaryEvidence = null,
  verifierEvidence = null,
}) {
  const planned = controller.releaseNext({ sessionToken, boundaryEvidence });
  if (planned.stage_id !== `S${scheduleIndex + 1}`) throw new Error("Stage-controller sequence mismatch");
  const releaseContent = await fs.readFile(path.join(PROJECT_ROOT, planned.release_file));
  const release = JSON.parse(releaseContent.toString("utf8"));
  if (release.stage_id !== planned.stage_id || release.test_only !== true) throw new Error(`Release identity mismatch: ${planned.stage_id}`);
  await writeWorkspaceFile(workspace, `releases/${planned.stage_id}.json`, releaseContent);
  const inputInventory = await recursiveInventory(workspace);
  const request = {
    schema_version: 2,
    test_only: true,
    condition,
    horizon: "H4",
    stress_track: "EVOLVING_NEGOTIATION_STATE",
    stage_id: planned.stage_id,
    common_instruction_path: "instructions/common.md",
    verifier_evidence: verifierEvidence,
  };
  const startedAt = new Date().toISOString();
  const started = performance.now();
  const response = await worker.invoke({ stageId: planned.stage_id, verifierEvidence });
  const latency = performance.now() - started;
  const completedAt = new Date().toISOString();
  const parsed = parseStageOutput(response.result.raw_output, planned.stage_id);
  if (!parsed.valid) throw new Error(`Malformed TEST-ONLY stage output: ${parsed.reason}`);
  const outputContent = Buffer.from(`${JSON.stringify(parsed.output, null, 2)}\n`);
  await writeWorkspaceFile(workspace, `work-product/${planned.stage_id}.json`, outputContent);
  return {
    stage_id: planned.stage_id,
    sequence: planned.sequence,
    worker_pid: worker.pid,
    worker_session_token_sha256: sha256(sessionToken),
    release_file: planned.release_file,
    release_sha256: sha256(releaseContent),
    input_inventory_sha256: sha256(canonicalJson(inputInventory)),
    request_sha256: sha256(canonicalJson(request)),
    output_sha256: sha256(response.result.raw_output),
    receiver_output: parsed.output,
    verifier_evidence_supplied: verifierEvidence !== null,
    timestamps: { started_at: startedAt, completed_at: completedAt },
    telemetry: {
      wall_clock_latency_ms: latency,
      input_tokens: response.result.telemetry.input_tokens,
      output_tokens: response.result.telemetry.output_tokens,
      provider_cost_usd: response.result.telemetry.provider_cost_usd,
      provider_reported: response.result.telemetry.provider_reported,
    },
    model: response.metadata,
  };
}

function buildEpisodeRecord({ manifest, invocationId, condition, parity, episode }) {
  const invalidReasons = [];
  if (!parity.passed) invalidReasons.push("cross_arm_information_parity_failed");
  if (!episode.boundary.valid) invalidReasons.push("cold_boundary_failed");
  if (condition === "C2_PROOFPRESS" && episode.verifier.status !== "ok") invalidReasons.push("required_verifier_not_ok");
  const totalLatency = episode.stages.reduce((sum, stage) => sum + stage.telemetry.wall_clock_latency_ms, 0);
  return {
    schema_version: 2,
    record_type: "h4_calibration_episode",
    run_id: `${invocationId}-${condition}`,
    invocation_id: invocationId,
    test_only: true,
    publishable: false,
    condition,
    horizon: "H4",
    stress_track: "EVOLVING_NEGOTIATION_STATE",
    replicate: 1,
    matter: {
      candidate_id: manifest.candidate_matter.id,
      candidate_status: manifest.candidate_matter.status,
      fixture: "TEST-ONLY synthetic mechanics fixture",
      official_harvey_score: false,
    },
    stages: episode.stages,
    stage_controller: episode.stage_controller,
    workspace_boundaries: [episode.boundary],
    information_parity: parity,
    transferred_file_manifest: episode.boundary.transferred_file_manifest,
    verifier: episode.verifier,
    evaluation: {
      legal_rubric: {
        status: "NOT_RUN_TEST_ONLY",
        criteria: [],
        note: "The Harvey LAB evaluator was not run or simulated.",
      },
    },
    deterministic_score: null,
    timestamps: {
      episode_completed_at: new Date().toISOString(),
    },
    model: episode.stages.at(-1).model,
    telemetry: {
      wall_clock_latency_ms: totalLatency,
      input_tokens: null,
      output_tokens: null,
      provider_cost_usd: null,
      provider_reported: false,
      turns: episode.stages.length,
      document_reads: null,
    },
    invalid: {
      is_invalid: invalidReasons.length > 0,
      reason: invalidReasons.join("+") || null,
    },
    result_file: `TEST-ONLY-${condition}.json`,
  };
}

function unavailableVerifier() {
  return {
    required: false,
    test_only: true,
    pin_verified: null,
    status: "not_available_in_C1",
    malformed: false,
    duration_ms: null,
    commands: [],
    claim_scope: "C1 has no provenance verifier; no verifier result is inferred.",
  };
}

async function readPackage(workspace) {
  const inventory = await recursiveInventory(workspace);
  const files = [];
  for (const item of inventory.filter((entry) => entry.type === "file")) {
    files.push({ path: item.path, content: await fs.readFile(path.join(workspace, item.path)) });
  }
  return files.sort((a, b) => a.path.localeCompare(b.path));
}

async function copyPackage(files, workspace) {
  for (const file of files) await writeWorkspaceFile(workspace, file.path, file.content);
}

async function writeWorkspaceFile(workspace, relativePath, content) {
  const destination = path.join(workspace, relativePath);
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.writeFile(destination, content, { flag: "wx" });
}

function enforceOutputBoundary(output) {
  const segments = output.split(path.sep).map((segment) => segment.toLowerCase());
  if (!segments.includes("test-only")) throw new Error("TEST-ONLY output path must contain a test-only directory segment");
}

async function ensureOutputDirectory(output) {
  await fs.mkdir(output, { recursive: true });
  const entries = await fs.readdir(output);
  if (entries.some((name) => name.endsWith(".json"))) throw new Error(`Output directory already contains JSON records: ${output}`);
}

async function exists(target) {
  try {
    await fs.access(target);
    return true;
  } catch {
    return false;
  }
}
