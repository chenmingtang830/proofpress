import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { createClaudeCliAdapter } from "../adapters/claude-cli.mjs";
import { createVercelGatewayAdapter } from "../adapters/vercel-ai-gateway.mjs";
import { assertResponseEligible } from "./response-eligibility.mjs";

const execFileAsync = promisify(execFile);

export async function runPrepare({ packetDir, output, manifest, trackId, authorizeRealCalls, root,
  env = process.env, adapterOverride = null, judgeOverride = null, sharedSenderFrom = null }) {
  requireAuthorization(authorizeRealCalls, manifest);
  await fs.mkdir(path.dirname(output), { recursive: true });
  await fs.mkdir(output, { recursive: false });
  const packet = JSON.parse(await fs.readFile(path.join(packetDir, "RUN_PACKET.json")));
  const promptContract = await fs.readFile(path.join(packetDir, "PROMPT_CONTRACT.md"), "utf8");
  const adapter = adapterOverride ?? adapterFor(manifest, trackId);
  const judge = judgeOverride ?? createVercelGatewayAdapter(manifest.policy_gate.judge);
  const receiverStart = receiverSourceStart(packet);
  const senderStageIds = packet.stages.slice(0, receiverStart).map((stage) => stage.stage_id);
  // Freeze one sender trajectory, then fork the handoff treatment. Generating
  // separate sender work per condition would confound handoff effects with
  // sender sampling variance.
  const workspace = path.join(output, "sender", "SHARED_SENDER");
  await fs.mkdir(workspace, { recursive: true });
  await copyStageSources(packetDir, workspace, senderStageIds);
  const sharedStages = [];
  let prior = "No prior stage output.";
  let senderReuse = null;
  let reusedSourceState = null;
  let reusedSourcePacket = null;
  if (sharedSenderFrom) {
    const sourceRoot = path.resolve(sharedSenderFrom);
    let sourceState = null;
    try { sourceState = JSON.parse(await fs.readFile(path.join(sourceRoot, "RUN_STATE.json"))); }
    catch (error) { if (error.code !== "ENOENT") throw error; }
    const sourcePacket = sourceState
      ? JSON.parse(await fs.readFile(path.join(sourceState.packet_dir, "RUN_PACKET.json")))
      : packet;
    reusedSourceState = sourceState;
    reusedSourcePacket = sourcePacket;
    if (sourceState && sourceState.track_id !== trackId) throw new Error("reused sender track does not match requested track");
    if (sourcePacket.harvey.task_id !== packet.harvey.task_id) throw new Error("reused sender task does not match packet task");
    const senderSet = new Set(senderStageIds);
    const sourceStages = sourceState
      ? sourceState.episodes.C1_ORDINARY_PORTABLE.stages.filter((x) => senderSet.has(x.stage_id))
      : await Promise.all(senderStageIds.map(async (stageId) => {
          const response = JSON.parse(await fs.readFile(path.join(sourceRoot, "sender", "SHARED_SENDER",
            `MODEL_RESPONSE_${stageId}.json`)));
          return { stage_id: stageId, output: parseWorkerOutput(response.raw_output, stageId), telemetry: response.telemetry };
        }));
    if (sourceStages.length !== senderStageIds.length
      || sourceStages.map((x) => x.stage_id).join(",") !== senderStageIds.join(","))
      throw new Error(`reused sender state must contain exactly ${senderStageIds.join(",")}`);
    sharedStages.push(...structuredClone(sourceStages));
    prior = sharedStages.at(-1).output.summary;
    for (const stageId of senderStageIds)
      await fs.copyFile(path.join(sourceRoot, "sender", "SHARED_SENDER", `MODEL_RESPONSE_${stageId}.json`),
        path.join(workspace, `MODEL_RESPONSE_${stageId}.json`), fs.constants.COPYFILE_EXCL);
    senderReuse = { source_run: sourceRoot, source_experiment_id: sourceState?.experiment_id ?? sourcePacket.experiment_id,
      source_status: sourceState?.status ?? "RECOVERED_FROM_FAILED_RUN_BEFORE_STATE_WRITE",
      track_id: sourceState?.track_id ?? trackId,
      task_id: sourcePacket.harvey.task_id };
  } else {
    for (const stageId of senderStageIds) {
      const sourcePacket = await stageEvidencePacket(root, packetDir, packet, stageId);
      const result = await adapter.invoke({ prompt: stagePrompt({ promptContract, packet, stageId,
        condition: "SHARED_SENDER", prior, sourcePacket }) }, { workspace, env });
      await fs.writeFile(path.join(workspace, `MODEL_RESPONSE_${stageId}.json`), `${JSON.stringify(result, null, 2)}\n`, { flag: "wx" });
      assertForAdapter(result, adapter, adapter.metadata().max_output_tokens, `sender ${stageId}`);
      const parsed = parseWorkerOutput(result.raw_output, stageId);
      sharedStages.push({ stage_id: stageId, output: parsed, telemetry: result.telemetry });
      prior = parsed.summary;
    }
  }
  const episodes = Object.fromEntries(packet.conditions.map((condition) => [condition, {
    sender_state: "SHARED_SENDER",
    stages: structuredClone(sharedStages),
    raw_handoff: condition === "C1_ORDINARY_PORTABLE" && packet.stress
      ? `${prior}\n\n${packet.stress.raw_handoff_text}`
      : prior,
  }]));
  for (const condition of packet.conditions) {
    if (condition === "C2_PROOFPRESS") {
      const ledger = path.join(output, "ledger-c2");
      const reusableC2 = reusedSourceState?.episodes?.C2_PROOFPRESS;
      const reusableLedger = reusableC2?.ledger;
      const sourceStressId = reusedSourcePacket?.stress?.id ?? null;
      const targetStressId = packet.stress?.id ?? null;
      if (sourceStressId && sourceStressId !== targetStressId)
        throw new Error("cannot reuse a sender ledger carrying a different stress fixture");
      const reuseGovernance = reusableLedger && await pathExists(reusableLedger);
      let evidence;
      let conclusions;
      let baseProposals = [];
      if (reuseGovernance) {
        await fs.cp(reusableLedger, ledger, { recursive: true, errorOnExist: true });
        baseProposals = structuredClone(reusableC2.proposals ?? []);
        evidence = new Map(baseProposals.flatMap((proposal) => proposal.evidence_files.map((name, index) =>
          [name, proposal.evidence_refs[index]])).filter(([, ref]) => ref));
        conclusions = [];
        episodes[condition].governance_reuse = {
          source_run: path.resolve(sharedSenderFrom),
          source_ledger: reusableLedger,
          source_judge_receipt: reusableC2.judge_transaction?.receipt ?? null,
          source_conclusion_count: baseProposals.length,
        };
      } else {
        await initLedger(ledger);
        evidence = await importSources(root, ledger, path.join(packetDir, "source"), senderStageIds);
        conclusions = consolidateConclusions(sharedStages.flatMap((s) => s.output.conclusions));
      }
      if (packet.stress && sourceStressId !== targetStressId) {
        const stressPath = path.join(packetDir, packet.stress.artifact_path);
        evidence.set(packet.stress.artifact_filename,
          await importOneSource(root, ledger, stressPath, new Set(evidence.values())));
        conclusions.push({ statement: packet.stress.statement,
          evidence_files: [packet.stress.artifact_filename],
          expires_at: packet.stress.ledger_control?.expires_at ?? packet.stress.expires_at,
          stress_fixture_id: packet.stress.id });
      }
      const pending = [];
      for (const conclusion of conclusions) {
        conclusion.evidence_files = normalizeEvidenceFileNames(conclusion.evidence_files, [...evidence.keys()]);
        const refs = conclusion.evidence_files.map((name) => evidence.get(name)).filter(Boolean);
        if (!refs.length) throw new Error(`C2 conclusion has no bound evidence: ${conclusion.statement}`);
        const proposeArgs = ["propose", "--statement", conclusion.statement,
          ...refs.flatMap((ref) => ["--evidence", ref]), "--scope", packet.harvey.knowledge_scope,
          "--proposer", "agent:sender", "--allow-actor", "agent:receiver"];
        if (conclusion.expires_at) proposeArgs.push("--expires-at", conclusion.expires_at);
        const proposed = await proofpress(root, ledger, proposeArgs);
        const evaluation = await proofpress(root, ledger, ["evaluate", proposed.conclusion.id]);
        const evidencePacket = await extractEvidence(root,
          conclusion.evidence_files.map((name) => evidencePathForName(packetDir, packet, name)));
        pending.push({ conclusion, proposed, evaluation, evidencePacket, refs });
      }
      const proposals = [...baseProposals];
      if (pending.length) {
        const judgedBatch = await judge.invoke({ prompt: batchJudgePrompt({ manifest, pending }),
          reasoning_effort: "none", max_output_tokens: 64000,
          response_format: { type: "json_object" } }, { workspace, env });
        await fs.writeFile(path.join(workspace, "JUDGE_BATCH_RESPONSE.json"),
          `${JSON.stringify(judgedBatch, null, 2)}\n`, { flag: "wx" });
        assertForAdapter(judgedBatch, judge, 64000, "transaction batch judge");
        const batchVerdicts = parseBatchJudgeOutput(judgedBatch.raw_output, pending.map((x) => x.proposed.conclusion.id));
        const batchReceipt = `batch:${judgedBatch.telemetry.request_id ?? "unreported"}`;
        for (const item of pending) {
        const batchVerdict = batchVerdicts.get(item.proposed.conclusion.id);
        let verdict = { recommendation: batchVerdict.recommendation, rationale: batchVerdict.rationale };
        let individualReview = null;
        if (batchVerdict.risk_level === "high" || batchVerdict.recommendation === "escalate") {
          const individualReviewCap = manifest.policy_gate.transaction_review?.individual_re_review_max_output_tokens ?? 8000;
          const reviewed = await judge.invoke({ prompt: judgePrompt({ manifest, conclusion: item.conclusion,
            evidencePacket: item.evidencePacket }), reasoning_effort: "none",
            max_output_tokens: individualReviewCap }, { workspace, env });
          await fs.writeFile(path.join(workspace, `JUDGE_REVIEW_${item.proposed.conclusion.id}.json`),
            `${JSON.stringify(reviewed, null, 2)}\n`, { flag: "wx" });
          assertForAdapter(reviewed, judge, individualReviewCap, `individual policy review ${item.proposed.conclusion.id}`);
          verdict = parseJudgeOutput(reviewed.raw_output);
          individualReview = { trigger: batchVerdict.risk_level === "high" ? "high_risk" : "escalated",
            verdict, telemetry: reviewed.telemetry };
        }
        const gate = await researchPolicyAdmit(root, ledger, { conclusion_id: item.proposed.conclusion.id, verdict,
          executor: manifest.policy_gate.executor, judge: { route: manifest.policy_gate.judge.endpoint, model: manifest.policy_gate.judge.resolved_model } });
        proposals.push({ id: item.proposed.conclusion.id, statement: item.conclusion.statement,
          evidence_refs: item.refs, evidence_files: item.conclusion.evidence_files,
          stress_fixture_id: item.conclusion.stress_fixture_id ?? null,
          evaluation: item.evaluation, batch_verdict: batchVerdict, batch_receipt: batchReceipt,
          individual_review: individualReview, verdict, admitted: gate.admitted });
        }
        episodes[condition].judge_transaction = { receipt: batchReceipt, conclusion_count: pending.length,
          telemetry: judgedBatch.telemetry };
      }
      episodes[condition].ledger = ledger;
      episodes[condition].proposals = proposals;
    }
  }
  const state = { schema_version: 2, status: "POLICY_GATE_COMPLETE", experiment_id: manifest.id,
    track_id: trackId, packet_dir: packetDir, adapter: adapter.metadata(), sender_reuse: senderReuse, episodes };
  await fs.writeFile(path.join(output, "RUN_STATE.json"), `${JSON.stringify(state, null, 2)}\n`, { flag: "wx" });
  return state;
}

export async function runResume({ output, manifest, authorizeRealCalls, root, env = process.env, adapterOverride = null }) {
  requireAuthorization(authorizeRealCalls, manifest);
  const statePath = path.join(output, "RUN_STATE.json");
  const state = JSON.parse(await fs.readFile(statePath));
  if (state.status !== "POLICY_GATE_COMPLETE") throw new Error(`cannot resume state ${state.status}`);
  const adapter = adapterOverride ?? adapterFor(manifest, state.track_id);
  const packet = JSON.parse(await fs.readFile(path.join(state.packet_dir, "RUN_PACKET.json")));
  const trusted = await proofpress(root, state.episodes.C2_PROOFPRESS.ledger,
    ["context", "--scope", packet.harvey.knowledge_scope, "--actor", "agent:receiver", "--format", "json"]);
  const promptContract = await fs.readFile(path.join(state.packet_dir, "PROMPT_CONTRACT.md"), "utf8");
  const receiverStart = receiverSourceStart(packet);
  const firstReceiverStage = packet.stages[receiverStart].stage_id;
  for (const condition of packet.conditions) {
    const receiver = path.join(output, "receiver", condition);
    await fs.mkdir(receiver, { recursive: true });
    const receiverStages = packet.stages.slice(receiverStart).map((stage) => stage.stage_id);
    await copyStageSources(state.packet_dir, receiver, receiverStages);
    const inherited = condition === "C1_ORDINARY_PORTABLE"
      ? { raw_handoff: state.episodes[condition].raw_handoff,
          ...(packet.stress ? { boundary_memory_artifact: packet.stress.artifact_content ?? packet.stress } : {}) }
      : {};
    let selectedKnowledgeIds = [];
    if (condition === "C2_PROOFPRESS") {
      const selected = deterministicTraceSelection(trusted, 48);
      selectedKnowledgeIds = selected.knowledge_ids;
      const admitted = new Map(state.episodes.C2_PROOFPRESS.proposals.filter((x) => x.admitted).map((x) => [x.id, x]));
      const evidenceFiles = [...new Set(selected.knowledge_ids.flatMap((id) => admitted.get(id)?.evidence_files ?? []))];
      const knowledgeById = new Map(trusted.knowledge.map((x) => [x.id, x]));
      const expandedEvidence = await extractEvidence(root, evidenceFiles.map((name) =>
        path.join(state.packet_dir, "source", findStageForFile(packet, name), name)));
      const compiled = deterministicWorkingSet({ selected, knowledgeById, admitted });
      inherited.proofpress_governed_working_set = {
        schema_version: "proofpress/working-set/v1", ledger_head: trusted.ledger_head,
        scope: trusted.scope, policy_digest: trusted.policy_digest,
        ...compiled,
      };
      inherited.proofpress_trace_expansion = {
        selected_knowledge_ids: selected.knowledge_ids,
        rationale: selected.rationale,
        evidence_refs_resolved: Object.keys(expandedEvidence),
      };
      state.episodes.C2_PROOFPRESS.trace_lookup = { ...selected, evidence_files: evidenceFiles,
        telemetry: null, compiler_telemetry: null, assembly: "deterministic-v10" };
    }
    await fs.writeFile(path.join(receiver, "INHERITED_CONTEXT.json"), `${JSON.stringify(inherited, null, 2)}\n`);
    let prior = JSON.stringify(inherited);
    for (const stageId of receiverStages) {
      const sourcePacket = await stageEvidencePacket(root, state.packet_dir, packet, stageId, receiverStart);
      const responsePath = path.join(receiver, `MODEL_RESPONSE_${stageId}.json`);
      let result;
      try {
        result = JSON.parse(await fs.readFile(responsePath, "utf8"));
      } catch (error) {
        if (error.code !== "ENOENT") throw error;
        result = await adapter.invoke({
          prompt: stagePrompt({ promptContract, packet, stageId, condition, prior, sourcePacket }),
          ...(stageId === "S4" ? { max_output_tokens: adapter.metadata().final_stage_max_output_tokens } : {}),
        }, { workspace: receiver, env });
        await fs.writeFile(responsePath, `${JSON.stringify(result, null, 2)}\n`, { flag: "wx" });
      }
      const workerCap = stageId === "S4"
        ? adapter.metadata().final_stage_max_output_tokens
        : adapter.metadata().max_output_tokens;
      assertForAdapter(result, adapter, workerCap, `${condition} worker ${stageId}`);
      const parsed = parseWorkerOutput(result.raw_output, stageId);
      state.episodes[condition].stages.push({ stage_id: stageId, output: parsed, telemetry: result.telemetry });
      prior = parsed.summary;
      if (stageId === "S4") {
        const markdown = path.join(receiver, "escalation-approval-memo.md");
        const docx = path.join(receiver, packet.harvey.final_deliverable);
        await fs.writeFile(markdown, parsed.final_markdown);
        // GFM disables Pandoc's YAML metadata extension. A valid deliverable may
        // begin with a thematic break (`---`), which default Pandoc Markdown
        // otherwise misreads as an unterminated YAML metadata block.
        await execFileAsync("pandoc", ["--from=markdown-yaml_metadata_block", markdown, "-o", docx]);
        state.episodes[condition].deliverable = docx;
      }
    }
  }
  state.status = "READY_FOR_LAB_EVALUATION";
  state.policy_gate = { mode: manifest.policy_gate.mode, executor: manifest.policy_gate.executor,
    decisions: state.episodes.C2_PROOFPRESS.proposals.map(({ id, verdict, admitted }) => ({ conclusion: id, verdict, admitted })) };
  await fs.writeFile(statePath, `${JSON.stringify(state, null, 2)}\n`);
  return state;
}

function adapterFor(manifest, id) {
  const track = manifest.tracks.find((item) => item.id === id);
  if (!track) throw new Error(`unknown track ${id}`);
  return track.route === "local Claude CLI"
    ? createClaudeCliAdapter(track.adapter)
    : createVercelGatewayAdapter(track.adapter);
}
function assertForAdapter(result, adapter, outputCap, label) {
  const metadata = adapter.metadata();
  return assertResponseEligible(result, {
    label,
    outputCap,
    requestedModel: metadata.resolved_model,
    requestedProvider: metadata.serving_provider_only,
  });
}
function requireAuthorization(flag, manifest) {
  if (!flag) throw new Error("real model calls require --authorize-real-calls");
  if (manifest.real_calls_authorized !== false) throw new Error("manifest safety invariant changed; expected real_calls_authorized=false");
}
function parseJudgeOutput(raw) {
  let value; try { value = JSON.parse(jsonPayload(raw)); } catch { throw new Error("policy judge returned invalid JSON"); }
  if (!["accept", "reject", "escalate"].includes(value.recommendation) || typeof value.rationale !== "string" || !value.rationale.trim())
    throw new Error("policy judge must return recommendation accept|reject|escalate and rationale");
  return { recommendation: value.recommendation, rationale: value.rationale };
}
function judgePrompt({ manifest, conclusion, evidencePacket }) {
  return `${manifest.policy_gate.prompt}\n\nConclusion: ${conclusion.statement}\nEvidence files: ${JSON.stringify(evidencePacket)}\n\nReturn ONLY JSON: {"recommendation":"accept|reject|escalate","rationale":"..."}.`;
}
function batchJudgePrompt({ manifest, pending }) {
  const evidenceCatalog = {};
  const conclusions = pending.map(({ conclusion, proposed, evaluation, evidencePacket }) => {
    Object.assign(evidenceCatalog, evidencePacket);
    return { conclusion_id: proposed.conclusion.id, statement: conclusion.statement,
      evidence_files: conclusion.evidence_files, deterministic_evaluation: evaluation };
  });
  return `${manifest.policy_gate.prompt}\n\nReview this transaction as one batch. Deterministic checks have already run per conclusion. Return one independent verdict for every conclusion. Mark risk_level high only when incorrect inheritance could create material legal, financial, compliance, authority, or irreversible-action risk. Keep each rationale to 25 words or fewer.\n\nConclusions:\n${JSON.stringify(conclusions)}\n\nDeduplicated evidence catalog:\n${JSON.stringify(evidenceCatalog)}\n\nReturn ONLY JSON: {"verdicts":[{"conclusion_id":"knw_...","recommendation":"accept|reject|escalate","risk_level":"low|medium|high","rationale":"..."}]}. Include every supplied conclusion exactly once and no others.`;
}
function parseBatchJudgeOutput(raw, expectedIds) {
  let value; try { value = JSON.parse(jsonPayload(raw)); } catch { throw new Error("batch policy judge returned invalid JSON"); }
  if (!Array.isArray(value.verdicts)) throw new Error("batch policy judge must return verdicts");
  const expected = new Set(expectedIds); const seen = new Map();
  for (const row of value.verdicts) {
    if (!expected.has(row.conclusion_id) || seen.has(row.conclusion_id))
      throw new Error("batch policy judge returned unknown or duplicate conclusion_id");
    if (!["accept", "reject", "escalate"].includes(row.recommendation)
      || !["low", "medium", "high"].includes(row.risk_level)
      || typeof row.rationale !== "string" || !row.rationale.trim())
      throw new Error("batch policy verdict has invalid recommendation, risk_level, or rationale");
    seen.set(row.conclusion_id, row);
  }
  if (seen.size !== expected.size) throw new Error("batch policy judge omitted one or more conclusions");
  return seen;
}
function parseCompiledWorkingSet(raw, allowedKnowledgeIds, allowedEvidenceFiles) {
  let value; try { value = JSON.parse(jsonPayload(raw)); } catch { throw new Error("working-set compiler returned invalid JSON"); }
  if (!Array.isArray(value.requirements) || !Array.isArray(value.open_gaps))
    throw new Error("working-set compiler must return requirements and open_gaps");
  const knowledge = new Set(allowedKnowledgeIds); const evidence = new Set(allowedEvidenceFiles);
  for (const row of value.requirements) {
    if (typeof row.requirement !== "string" || typeof row.synthesis !== "string"
      || !Array.isArray(row.knowledge_ids) || !Array.isArray(row.evidence_files)
      || row.knowledge_ids.some((id) => !knowledge.has(id))
      || row.evidence_files.some((name) => !evidence.has(name)))
      throw new Error("working-set compiler returned unsupported lineage references");
  }
  return value;
}
function parseTraceSelection(raw, trusted, maxIds, excludedIds = []) {
  let value; try { value = JSON.parse(jsonPayload(raw)); } catch { throw new Error("trace selector returned invalid JSON"); }
  if (!Array.isArray(value.selected_knowledge_ids) || !Array.isArray(value.checklist) || typeof value.rationale !== "string")
    throw new Error("trace selector must return checklist, selected_knowledge_ids, and rationale");
  const allowed = new Set(trusted.knowledge.map((x) => x.id));
  const excluded = new Set(excludedIds);
  const ids = [...new Set(value.selected_knowledge_ids)].filter((id) => !excluded.has(id));
  if (ids.length > maxIds || ids.some((id) => !allowed.has(id)))
    throw new Error("trace selector requested unknown or too many knowledge receipts");
  for (const row of value.checklist) {
    if (typeof row.requirement !== "string" || !["covered", "gap"].includes(row.coverage)
      || !Array.isArray(row.knowledge_ids) || row.knowledge_ids.some((id) => !allowed.has(id)))
      throw new Error("trace selector returned an invalid checklist");
  }
  return { knowledge_ids: ids, checklist: value.checklist, rationale: value.rationale };
}
export function deterministicTraceSelection(trusted, maxIds, excludedIds = []) {
  const excluded = new Set(excludedIds);
  const candidates = trusted.knowledge.filter((row) => !excluded.has(row.id));
  const selected = candidates.slice(0, maxIds).map((row) => row.id);
  return {
    knowledge_ids: selected,
    checklist: [{ requirement: "Current admitted governed knowledge at the receiver boundary",
      knowledge_ids: selected, coverage: candidates.length <= maxIds ? "covered" : "gap" }],
    rationale: `Deterministic ledger-order selection: ${selected.length}/${candidates.length} current admitted receipts.`,
  };
}
function deterministicWorkingSet({ selected, knowledgeById, admitted }) {
  return {
    requirements: selected.knowledge_ids.map((id) => ({
      requirement: "Governed conclusion",
      synthesis: knowledgeById.get(id)?.statement ?? knowledgeById.get(id)?.content ?? "",
      knowledge_ids: [id],
      evidence_files: admitted.get(id)?.evidence_files ?? [],
    })),
    open_gaps: selected.checklist.filter((row) => row.coverage === "gap").map((row) => row.requirement),
  };
}
function findStageForFile(packet, name) {
  const stage = packet.stages.find((item) => item.release.includes(name));
  if (!stage) throw new Error(`evidence file not in frozen release schedule: ${name}`);
  return stage.stage_id;
}
function consolidateConclusions(rows) {
  const byStatement = new Map();
  for (const row of rows) {
    const existing = byStatement.get(row.statement);
    if (!existing) byStatement.set(row.statement, { ...row, evidence_files: [...new Set(row.evidence_files)] });
    else existing.evidence_files = [...new Set([...existing.evidence_files, ...row.evidence_files])];
  }
  return [...byStatement.values()];
}
export function normalizeEvidenceFileNames(names, availableNames) {
  const available = new Set(availableNames);
  const byBase = new Map();
  for (const name of availableNames) {
    const base = path.basename(name);
    const matches = byBase.get(base) ?? [];
    matches.push(name);
    byBase.set(base, matches);
  }
  return [...new Set(names.map((name) => {
    if (available.has(name)) return name;
    const matches = byBase.get(path.basename(name)) ?? [];
    if (matches.length === 1) return matches[0];
    const annotated = availableNames.filter((candidate) => {
      const suffix = name.slice(candidate.length).trim();
      return name.startsWith(candidate) && /^\([^)]*\)$/.test(suffix);
    });
    if (annotated.length !== 1) throw new Error(`unknown or ambiguous evidence filename: ${name}`);
    return annotated[0];
  }))];
}
function evidencePathForName(packetDir, packet, name) {
  if (packet.stress?.artifact_filename === name) return path.join(packetDir, packet.stress.artifact_path);
  return path.join(packetDir, "source", findStageForFile(packet, name), name);
}
async function extractEvidence(root, paths) {
  const { stdout } = await execFileAsync("python3", [path.join(root, "studies/long-horizon-eval/relaybench/bench/real/extract-evidence.py"),
    JSON.stringify({ paths, max_chars_per_file: 12000 })], { maxBuffer: 16 * 1024 * 1024 });
  return JSON.parse(stdout);
}
async function stageEvidencePacket(root, packetDir, packet, stageId, startIndex = 0) {
  const index = packet.stages.findIndex((item) => item.stage_id === stageId);
  if (index < 0) throw new Error(`unknown stage ${stageId}`);
  if (startIndex < 0 || startIndex > index) throw new Error(`invalid visible stage range for ${stageId}`);
  const paths = packet.stages.slice(startIndex, index + 1).flatMap((stage) =>
    stage.release.map((name) => path.join(packetDir, "source", stage.stage_id, name)));
  return extractEvidence(root, paths);
}
function receiverSourceStart(packet) {
  const index = packet.stages.findIndex((stage) => stage.cold_boundary_before === true);
  if (index < 1) throw new Error("packet must place one cold boundary after at least one sender stage");
  if (packet.stages.slice(index + 1).some((stage) => stage.cold_boundary_before === true))
    throw new Error("packet must contain exactly one cold boundary");
  return index;
}
async function researchPolicyAdmit(root, cwd, packet) {
  const { stdout } = await execFileAsync("python3", [path.join(root, "studies/long-horizon-eval/relaybench/bench/real/research-policy-admit.py"),
    JSON.stringify(packet)], { cwd, maxBuffer: 16 * 1024 * 1024 });
  return JSON.parse(stdout);
}
async function pathExists(target) {
  try { await fs.access(target); return true; } catch { return false; }
}
async function initLedger(cwd) {
  await fs.mkdir(cwd, { recursive: true });
  await execFileAsync("git", ["init", "-q"], { cwd });
  await execFileAsync("git", ["config", "user.email", "relaybench@proofpress.local"], { cwd });
  await execFileAsync("git", ["config", "user.name", "RelayBench"], { cwd });
  await fs.writeFile(path.join(cwd, "README.md"), "Proofpress C2 experiment ledger\n");
  await execFileAsync("git", ["add", "README.md"], { cwd }); await execFileAsync("git", ["commit", "-qm", "init"], { cwd });
}
async function proofpress(root, cwd, args) {
  const { stdout } = await execFileAsync(process.execPath, [path.join(root, "bin/proofpress.js"), ...args], { cwd, maxBuffer: 16 * 1024 * 1024 });
  return JSON.parse(stdout);
}
async function importSources(root, ledger, sourceRoot, stages) {
  const map = new Map(); let previous = new Set();
  for (const stage of stages) for (const name of await fs.readdir(path.join(sourceRoot, stage))) {
    const result = await proofpress(root, ledger, ["evidence", "import", path.join(sourceRoot, stage, name)]);
    const current = new Set(result.evidence); const added = [...current].filter((x) => !previous.has(x));
    if (added.length !== 1) throw new Error(`expected one evidence receipt for ${name}`);
    map.set(name, added[0]); previous = current;
  } return map;
}
async function importOneSource(root, ledger, sourcePath, previous) {
  const result = await proofpress(root, ledger, ["evidence", "import", sourcePath]);
  const current = new Set(result.evidence); const added = [...current].filter((x) => !previous.has(x));
  if (added.length !== 1) throw new Error(`expected one evidence receipt for ${path.basename(sourcePath)}`);
  return added[0];
}
async function copyStageSources(packetDir, workspace, stages) {
  for (const stage of stages) {
    const source = path.join(packetDir, "source", stage); const destination = path.join(workspace, "matter", stage);
    await fs.mkdir(path.dirname(destination), { recursive: true }); await fs.cp(source, destination, { recursive: true, errorOnExist: true });
  }
}
function stagePrompt({ promptContract, packet, stageId, condition, prior, sourcePacket }) {
  const stage = packet.stages.find((x) => x.stage_id === stageId);
  const deliverableRule = stageId === "S4"
    ? "S4 is the only deliverable stage. Return the complete final memo directly as Markdown, with no JSON envelope or code fence."
    : `${stageId} is not a deliverable stage: final_markdown MUST be an empty string. Do not draft or preview the final memo.`;
  const responseRule = stageId === "S4" ? "" : " Keep summary under 2,500 words, return at most 48 conclusions, and keep each conclusion under 100 words. Return ONLY JSON: {\"stage_id\":\"" + stageId + "\",\"summary\":\"...\",\"conclusions\":[{\"statement\":\"...\",\"evidence_files\":[\"filename\"]}],\"final_markdown\":\"\"}.";
  return `${promptContract}\n\nCondition: ${condition}\nCurrent stage: ${stageId} — ${stage.label}\nNew files: ${stage.release.join(", ")}\nInherited state:\n${prior}\n\nReleased source text (deterministically extracted; no later-stage files are present):\n${JSON.stringify(sourcePacket)}\n\n${deliverableRule}${responseRule}`;
}
function parseWorkerOutput(raw, stageId) {
  if (stageId === "S4") {
    const text = String(raw).trim();
    try {
      const legacy = JSON.parse(jsonPayload(text));
      if (legacy.stage_id === "S4" && typeof legacy.final_markdown === "string") return legacy;
    } catch {}
    if (!text) throw new Error("S4 final Markdown is required");
    return { stage_id: "S4", summary: "Complete final deliverable.", conclusions: [], final_markdown: text };
  }
  let value; try { value = JSON.parse(jsonPayload(raw)); } catch { throw new Error(`model returned invalid JSON at ${stageId}`); }
  if (value.stage_id !== stageId || typeof value.summary !== "string" || !Array.isArray(value.conclusions)) throw new Error(`invalid worker output at ${stageId}`);
  if (stageId === "S4" && typeof value.final_markdown !== "string") throw new Error("S4 final_markdown is required");
  if (stageId !== "S4" && value.final_markdown !== "") throw new Error(`${stageId} final_markdown must be empty`);
  return value;
}
function jsonPayload(raw) {
  const text = String(raw).trim();
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fenced) return fenced[1].trim();
  const start = text.indexOf("{"); const end = text.lastIndexOf("}");
  return start >= 0 && end > start ? text.slice(start, end + 1) : text;
}
