import fs from "node:fs/promises";
import path from "node:path";
import { canonicalJson, readJson, sha256File } from "../lib/core.mjs";

const CONDITIONS = ["C1_ORDINARY_PORTABLE", "C2_PROOFPRESS"];

export async function prepareRealPacket({ manifestPath, harveyCheckout, output }) {
  const manifest = await readJson(manifestPath);
  const candidate = await readJson(path.resolve(path.dirname(manifestPath), "../fixtures/h4-msa-escalation-candidate/candidate.json"));
  await fs.mkdir(output, { recursive: false });
  const taskRoot = path.join(harveyCheckout, candidate.harvey_lab.task_id.replace(/^contracts\//, "tasks/contracts/"));
  const task = await readJson(path.join(taskRoot, "task.json"));
  const copied = [];
  for (const stage of candidate.proposed_h4_release_schedule) {
    for (const name of stage.release) {
      const source = path.join(taskRoot, "documents", name);
      const destination = path.join(output, "source", stage.stage_id, name);
      await fs.mkdir(path.dirname(destination), { recursive: true });
      await fs.copyFile(source, destination, fs.constants.COPYFILE_EXCL);
      copied.push({ stage_id: stage.stage_id, path: `source/${stage.stage_id}/${name}`,
        sha256: await sha256File(destination) });
    }
  }
  const packet = {
    schema_version: 1, experiment_id: manifest.id, created_at: new Date().toISOString(),
    harvey: { repository: manifest.task_selection.repository, commit: manifest.task_selection.commit,
      task_id: candidate.harvey_lab.task_id, task_title: task.title,
      official_public_criteria: task.criteria.length, final_deliverable: candidate.harvey_lab.final_deliverable },
    conditions: CONDITIONS, tracks: manifest.tracks.map(({ id, route, adapter }) => ({ id, route,
      resolved_model: adapter.resolved_model, fallback: adapter.fallback, retries: adapter.retries })),
    stages: candidate.proposed_h4_release_schedule.map((stage) => ({ ...stage,
      prompt_contract: stage.stage_id === "S4" ? "produce final memo as Markdown for deterministic pandoc conversion to DOCX" : "produce JSON conclusions and a readable handoff summary" })),
    copied_sources: copied, review_gate: manifest.review_gate,
    parity_contract: "C1 and C2 receive byte-identical source releases; only C2 receives governed context emitted by proofpress context",
    payable_calls_authorized: false,
  };
  await fs.writeFile(path.join(output, "RUN_PACKET.json"), `${JSON.stringify(packet, null, 2)}\n`, { flag: "wx" });
  await fs.writeFile(path.join(output, "HUMAN_REVIEW.template.json"), `${JSON.stringify({
    schema_version: 1, experiment_id: manifest.id, reviewer: manifest.review_gate.reviewer_role,
    decisions: [], attestation: "I reviewed the evidence-bound conclusions and recorded these decisions.",
    signed_at: null,
  }, null, 2)}\n`, { flag: "wx" });
  await fs.writeFile(path.join(output, "PROMPT_CONTRACT.md"), promptContract(task.instructions), { flag: "wx" });
  return { packet, packet_digest_input: canonicalJson(packet), output };
}

function promptContract(instructions) {
  return `# Frozen worker contract\n\n${instructions}\n\n## Long-horizon controls\n\n- Use only files released for the current stage.\n- Do not infer hidden state or consult prior transcripts.\n- Before S3 the sender process and workspace are destroyed.\n- C1 receives the readable raw handoff. C2 receives only Proofpress trusted context.\n- Cite source filename and operative version for every reusable conclusion.\n- At S4 return Markdown suitable for deterministic conversion to the required DOCX.\n`;
}
