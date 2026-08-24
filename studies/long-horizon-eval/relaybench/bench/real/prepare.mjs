import fs from "node:fs/promises";
import path from "node:path";
import { canonicalJson, readJson, sha256File } from "../lib/core.mjs";

const CONDITIONS = ["C1_ORDINARY_PORTABLE", "C2_PROOFPRESS"];

export async function prepareRealPacket({ manifestPath, harveyCheckout, output, candidatePath = null,
  stressFixturePath = null, coldBoundaryBefore = null }) {
  const manifest = await readJson(manifestPath);
  const candidate = await readJson(candidatePath
    ? path.resolve(candidatePath)
    : path.resolve(path.dirname(manifestPath), "../fixtures/h4-msa-escalation-candidate/candidate.json"));
  const stress = stressFixturePath ? await readJson(path.resolve(stressFixturePath)) : null;
  if (stress && stress.task_id !== candidate.harvey_lab.task_id)
    throw new Error(`stress fixture task ${stress.task_id} does not match candidate ${candidate.harvey_lab.task_id}`);
  const schedule = candidate.proposed_h4_release_schedule.map((stage) => ({ ...stage,
    cold_boundary_before: coldBoundaryBefore ? stage.stage_id === coldBoundaryBefore : stage.cold_boundary_before }));
  if (coldBoundaryBefore && !schedule.some((stage) => stage.stage_id === coldBoundaryBefore))
    throw new Error(`unknown cold boundary stage ${coldBoundaryBefore}`);
  if (schedule.filter((stage) => stage.cold_boundary_before).length !== 1)
    throw new Error("release schedule must contain exactly one cold boundary");
  await fs.mkdir(output, { recursive: false });
  const taskRoot = path.join(harveyCheckout, candidate.harvey_lab.task_id.replace(/^contracts\//, "tasks/contracts/"));
  const task = await readJson(path.join(taskRoot, "task.json"));
  const copied = [];
  for (const stage of schedule) {
    for (const name of stage.release) {
      const source = path.join(taskRoot, "documents", name);
      const destination = path.join(output, "source", stage.stage_id, name);
      await fs.mkdir(path.dirname(destination), { recursive: true });
      await fs.copyFile(source, destination, fs.constants.COPYFILE_EXCL);
      copied.push({ stage_id: stage.stage_id, path: `source/${stage.stage_id}/${name}`,
        sha256: await sha256File(destination) });
    }
  }
  let stressArtifact = null;
  if (stress) {
    const destination = path.join(output, "stress", stress.artifact_filename);
    await fs.mkdir(path.dirname(destination), { recursive: true });
    await fs.writeFile(destination, `${JSON.stringify(stress.artifact_content ?? stress, null, 2)}\n`, { flag: "wx" });
    stressArtifact = { path: `stress/${stress.artifact_filename}`, sha256: await sha256File(destination) };
  }
  const packet = {
    schema_version: 1, experiment_id: manifest.id, created_at: new Date().toISOString(),
    harvey: { repository: manifest.task_selection.repository, commit: manifest.task_selection.commit,
      task_id: candidate.harvey_lab.task_id, task_title: task.title,
      official_public_criteria: task.criteria.length, final_deliverable: candidate.harvey_lab.final_deliverable,
      knowledge_scope: `legal:lab:${candidate.harvey_lab.task_id}` },
    conditions: CONDITIONS, tracks: manifest.tracks.map(({ id, route, adapter }) => ({ id, route,
      resolved_model: adapter.resolved_model, fallback: adapter.fallback, retries: adapter.retries })),
    stages: schedule.map((stage) => ({ ...stage,
      prompt_contract: stage.stage_id === "S4" ? "produce final memo as Markdown for deterministic pandoc conversion to DOCX" : "produce JSON conclusions and a readable handoff summary" })),
    copied_sources: copied, policy_gate: manifest.policy_gate,
    study_arm: stress ? "LAB_DERIVED_CONTROLLED_HANDOFF_STRESS" : "UNMODIFIED_LAB_CLEAN_FIDELITY",
    cold_boundary_before: schedule.find((stage) => stage.cold_boundary_before).stage_id,
    stress: stress ? { ...stress, artifact_path: stressArtifact.path, artifact_sha256: stressArtifact.sha256 } : null,
    parity_contract: stress
      ? "C1 and C2 share one sender trajectory, the same frozen boundary perturbation artifact, byte-identical post-boundary source releases, model, caps, tools, and evaluator. C1 carries the perturbation as readable memory; C2 imports it into the ledger and applies frozen deterministic and policy gates before context emission. Neither receiver can reopen pre-boundary sources."
      : "C1 and C2 receive byte-identical post-boundary source releases; neither receiver can reopen pre-boundary sources; only C2 receives governed context emitted by proofpress context",
    payable_calls_authorized: false,
  };
  await fs.writeFile(path.join(output, "RUN_PACKET.json"), `${JSON.stringify(packet, null, 2)}\n`, { flag: "wx" });
  await fs.writeFile(path.join(output, "BLIND_POST_RUN_AUDIT.template.json"), `${JSON.stringify({
    schema_version: 1, experiment_id: manifest.id, role: manifest.policy_gate.human_role,
    run_complete: false, condition_labels_hidden: true, error_labels: [], signed_at: null,
  }, null, 2)}\n`, { flag: "wx" });
  await fs.writeFile(path.join(output, "PROMPT_CONTRACT.md"), promptContract(task.instructions), { flag: "wx" });
  return { packet, packet_digest_input: canonicalJson(packet), output };
}

function promptContract(instructions) {
  return `# Frozen worker contract\n\n${instructions}\n\n## Long-horizon controls\n\n- Use only files released to this process for the current or earlier visible stage.\n- Do not infer hidden state or consult prior transcripts.\n- At the declared cold boundary the sender process and workspace are destroyed; the receiver cannot reopen pre-boundary source files.\n- C1 receives the readable raw handoff. C2 receives only Proofpress trusted context.\n- Cite source filename and operative version for every reusable conclusion.\n- At S4 return Markdown suitable for deterministic conversion to the required DOCX.\n`;
}
