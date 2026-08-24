import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { createClaudeCliAdapter } from "../adapters/claude-cli.mjs";
import { createVercelGatewayAdapter } from "../adapters/vercel-ai-gateway.mjs";

const execFileAsync = promisify(execFile);

export async function runPrepare({ packetDir, output, manifest, trackId, authorizeRealCalls, root, env = process.env, adapterOverride = null }) {
  requireAuthorization(authorizeRealCalls, manifest);
  await fs.mkdir(output, { recursive: false });
  const packet = JSON.parse(await fs.readFile(path.join(packetDir, "RUN_PACKET.json")));
  const promptContract = await fs.readFile(path.join(packetDir, "PROMPT_CONTRACT.md"), "utf8");
  const adapter = adapterOverride ?? adapterFor(manifest, trackId);
  const episodes = {};
  for (const condition of packet.conditions) {
    const workspace = path.join(output, "sender", condition);
    await fs.mkdir(workspace, { recursive: true });
    await copyStageSources(packetDir, workspace, ["S1", "S2"]);
    const stages = [];
    let prior = "No prior stage output.";
    for (const stageId of ["S1", "S2"]) {
      const result = await adapter.invoke({ prompt: stagePrompt({ promptContract, packet, stageId, condition, prior }) }, { workspace, env });
      const parsed = parseWorkerOutput(result.raw_output, stageId);
      stages.push({ stage_id: stageId, output: parsed, telemetry: result.telemetry });
      prior = parsed.summary;
    }
    episodes[condition] = { stages, raw_handoff: prior };
    if (condition === "C2_PROOFPRESS") {
      const ledger = path.join(output, "ledger-c2");
      await initLedger(ledger);
      const evidence = await importSources(root, ledger, path.join(packetDir, "source"));
      const proposals = [];
      for (const conclusion of stages.flatMap((s) => s.output.conclusions)) {
        const refs = conclusion.evidence_files.map((name) => evidence.get(name)).filter(Boolean);
        if (!refs.length) throw new Error(`C2 conclusion has no bound evidence: ${conclusion.statement}`);
        const proposed = await proofpress(root, ledger, ["propose", "--statement", conclusion.statement,
          ...refs.flatMap((ref) => ["--evidence", ref]), "--scope", "legal:msa-escalation",
          "--proposer", "agent:sender", "--allow-actor", "agent:receiver"]);
        await proofpress(root, ledger, ["evaluate", proposed.conclusion.id]);
        proposals.push({ id: proposed.conclusion.id, statement: conclusion.statement, evidence_refs: refs });
      }
      episodes[condition].ledger = ledger;
      episodes[condition].proposals = proposals;
    }
  }
  const review = { schema_version: 1, experiment_id: manifest.id, reviewer: manifest.review_gate.reviewer_role,
    decisions: episodes.C2_PROOFPRESS.proposals.map(({ id }) => ({ conclusion: id, decision: null, note: null })),
    attestation: "I reviewed the evidence-bound conclusions and recorded these decisions.", signed_at: null };
  await fs.writeFile(path.join(output, "HUMAN_REVIEW.json"), `${JSON.stringify(review, null, 2)}\n`, { flag: "wx" });
  const state = { schema_version: 1, status: "AWAITING_HUMAN_REVIEW", experiment_id: manifest.id,
    track_id: trackId, packet_dir: packetDir, adapter: adapter.metadata(), episodes };
  await fs.writeFile(path.join(output, "RUN_STATE.json"), `${JSON.stringify(state, null, 2)}\n`, { flag: "wx" });
  return state;
}

export async function runResume({ output, manifest, authorizeRealCalls, root, env = process.env, adapterOverride = null }) {
  requireAuthorization(authorizeRealCalls, manifest);
  const statePath = path.join(output, "RUN_STATE.json");
  const state = JSON.parse(await fs.readFile(statePath));
  if (state.status !== "AWAITING_HUMAN_REVIEW") throw new Error(`cannot resume state ${state.status}`);
  const review = JSON.parse(await fs.readFile(path.join(output, "HUMAN_REVIEW.json")));
  validateHumanReview(review, state);
  const adapter = adapterOverride ?? adapterFor(manifest, state.track_id);
  for (const item of review.decisions) await proofpress(root, state.episodes.C2_PROOFPRESS.ledger,
    ["review", item.conclusion, item.decision === "admit" ? "--admit" : "--reject",
      "--reviewer", review.reviewer, "--note", item.note || "experiment review"]);
  const trusted = await proofpress(root, state.episodes.C2_PROOFPRESS.ledger,
    ["context", "--scope", "legal:msa-escalation", "--actor", "agent:receiver", "--format", "json"]);
  const packet = JSON.parse(await fs.readFile(path.join(state.packet_dir, "RUN_PACKET.json")));
  const promptContract = await fs.readFile(path.join(state.packet_dir, "PROMPT_CONTRACT.md"), "utf8");
  for (const condition of packet.conditions) {
    const receiver = path.join(output, "receiver", condition);
    await fs.mkdir(receiver, { recursive: true });
    await copyStageSources(state.packet_dir, receiver, ["S1", "S2", "S3", "S4"]);
    const inherited = condition === "C1_ORDINARY_PORTABLE"
      ? { raw_handoff: state.episodes[condition].raw_handoff }
      : { proofpress_trusted_context: trusted };
    await fs.writeFile(path.join(receiver, "INHERITED_CONTEXT.json"), `${JSON.stringify(inherited, null, 2)}\n`);
    let prior = JSON.stringify(inherited);
    for (const stageId of ["S3", "S4"]) {
      const result = await adapter.invoke({ prompt: stagePrompt({ promptContract, packet, stageId, condition, prior }) }, { workspace: receiver, env });
      const parsed = parseWorkerOutput(result.raw_output, stageId);
      state.episodes[condition].stages.push({ stage_id: stageId, output: parsed, telemetry: result.telemetry });
      prior = parsed.summary;
      if (stageId === "S4") {
        const markdown = path.join(receiver, "escalation-approval-memo.md");
        const docx = path.join(receiver, packet.harvey.final_deliverable);
        await fs.writeFile(markdown, parsed.final_markdown);
        await execFileAsync("pandoc", [markdown, "-o", docx]);
        state.episodes[condition].deliverable = docx;
      }
    }
  }
  state.status = "READY_FOR_LAB_EVALUATION";
  state.human_review = { reviewer: review.reviewer, signed_at: review.signed_at, decisions: review.decisions };
  await fs.writeFile(statePath, `${JSON.stringify(state, null, 2)}\n`);
  return state;
}

function adapterFor(manifest, id) {
  const track = manifest.tracks.find((item) => item.id === id);
  if (!track) throw new Error(`unknown track ${id}`);
  return id === "A_HARVEY_COMPARABLE" ? createClaudeCliAdapter(track.adapter) : createVercelGatewayAdapter(track.adapter);
}
function requireAuthorization(flag, manifest) {
  if (!flag) throw new Error("real model calls require --authorize-real-calls");
  if (manifest.real_calls_authorized !== false) throw new Error("manifest safety invariant changed; expected real_calls_authorized=false");
}
function validateHumanReview(review, state) {
  if (!review.signed_at || Number.isNaN(Date.parse(review.signed_at))) throw new Error("human review signed_at is required");
  if (!review.reviewer?.startsWith("human:")) throw new Error("reviewer must be a human identity");
  const expected = new Set(state.episodes.C2_PROOFPRESS.proposals.map((x) => x.id));
  if (review.decisions.length !== expected.size || review.decisions.some((x) => !expected.has(x.conclusion) || !["admit", "reject"].includes(x.decision)))
    throw new Error("human review must decide every proposed conclusion exactly once");
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
async function importSources(root, ledger, sourceRoot) {
  const map = new Map(); let previous = new Set();
  for (const stage of ["S1", "S2"]) for (const name of await fs.readdir(path.join(sourceRoot, stage))) {
    const result = await proofpress(root, ledger, ["evidence", "import", path.join(sourceRoot, stage, name)]);
    const current = new Set(result.evidence); const added = [...current].filter((x) => !previous.has(x));
    if (added.length !== 1) throw new Error(`expected one evidence receipt for ${name}`);
    map.set(name, added[0]); previous = current;
  } return map;
}
async function copyStageSources(packetDir, workspace, stages) {
  for (const stage of stages) {
    const source = path.join(packetDir, "source", stage); const destination = path.join(workspace, "matter", stage);
    await fs.mkdir(path.dirname(destination), { recursive: true }); await fs.cp(source, destination, { recursive: true, errorOnExist: true });
  }
}
function stagePrompt({ promptContract, packet, stageId, condition, prior }) {
  const stage = packet.stages.find((x) => x.stage_id === stageId);
  return `${promptContract}\n\nCondition: ${condition}\nCurrent stage: ${stageId} — ${stage.label}\nNew files: ${stage.release.join(", ")}\nInherited state:\n${prior}\n\nReturn ONLY JSON: {"stage_id":"${stageId}","summary":"...","conclusions":[{"statement":"...","evidence_files":["filename"]}],"final_markdown":"..."}. final_markdown is required only at S4.`;
}
function parseWorkerOutput(raw, stageId) {
  let value; try { value = JSON.parse(raw); } catch { throw new Error(`model returned invalid JSON at ${stageId}`); }
  if (value.stage_id !== stageId || typeof value.summary !== "string" || !Array.isArray(value.conclusions)) throw new Error(`invalid worker output at ${stageId}`);
  if (stageId === "S4" && typeof value.final_markdown !== "string") throw new Error("S4 final_markdown is required");
  return value;
}
