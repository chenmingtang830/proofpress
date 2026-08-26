#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const checkout = process.argv[2];
const out = process.argv[3];
if (!checkout || !out) throw new Error("usage: bench-freeze-14-task-expansion.mjs HARVEY_CHECKOUT OUTPUT_DIR");

const families = [
  ["credit", "contracts/financing/credit-lending-playbook-escalation"],
  ["msa", "contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation"],
  ["license", "contracts/ip-licensing/license-agreement-playbook-escalation"],
];

await fs.mkdir(out, { recursive: true });
const index = [];
for (const [family, taskBase] of families) {
  const root = path.join(checkout, "tasks", taskBase);
  const scenarios = (await fs.readdir(root, { withFileTypes: true }))
    .filter((entry) => entry.isDirectory() && /^scenario-\d+$/.test(entry.name))
    .map((entry) => entry.name).sort();
  for (const scenario of scenarios) {
    const taskId = `${taskBase}/${scenario}`;
    const taskRoot = path.join(root, scenario);
    const task = JSON.parse(await fs.readFile(path.join(taskRoot, "task.json"), "utf8"));
    const files = (await fs.readdir(path.join(taskRoot, "documents"))).sort();
    const stages = Object.fromEntries(["S1", "S2", "S3", "S4"].map((stage) => [stage, []]));
    for (const file of files) stages[classify(file)].push(file);
    const assigned = Object.values(stages).flat();
    if (new Set(assigned).size !== files.length || assigned.length !== files.length)
      throw new Error(`non-bijective release schedule for ${taskId}`);
    const finalDeliverable = outputName(task.instructions);
    const candidate = {
      schema_version: 1,
      selection_rule_id: "proofpress-deepseek-14-task-expansion-v1",
      harvey_lab: { task_id: taskId, final_deliverable: finalDeliverable },
      proposed_h4_release_schedule: [
        stage("S1", "Establish governing policy, authority, baseline terms, and original deal context", stages.S1),
        stage("S2", "Incorporate negotiated drafts, redlines, and negotiation history", stages.S2),
        stage("S3", "Revalidate against risk, financial, legal, and business evidence", stages.S3),
        stage("S4", "Prepare the requested escalation deliverable", stages.S4, true),
      ],
    };
    const name = `${family}-${scenario}.json`;
    await fs.writeFile(path.join(out, name), `${JSON.stringify(candidate, null, 2)}\n`);
    index.push({ family, scenario, task_id: taskId, title: task.title,
      criteria: task.criteria.length, candidate: `candidates-14/${name}`,
      release_counts: Object.fromEntries(Object.entries(stages).map(([key, value]) => [key, value.length])) });
  }
}
if (index.length !== 14) throw new Error(`expected 14 scenarios, found ${index.length}`);
await fs.writeFile(path.join(path.dirname(out), "deepseek-14-task-expansion-v1.json"), `${JSON.stringify({
  schema_version: 1,
  id: "proofpress-deepseek-14-task-expansion-v1",
  frozen_at: new Date().toISOString(),
  status: "FROZEN_BEFORE_EXPANSION_OUTCOMES",
  parent_protocol: "treatment-effect-protocol-v9.json",
  design: {
    arm: "clean",
    paired_runs_per_scenario: 1,
    cold_boundary_before: "S4",
    conditions: ["C1_ORDINARY_PORTABLE", "C2_PROOFPRESS"],
    purpose: "Task breadth and heterogeneity across all public scenarios in the three predeclared LAB Contracts families; not a stress test and not an official Harvey leaderboard result.",
  },
  model: {
    track: "R_DEEPSEEK_14_TASK_EXPANSION",
    resolved_model: "deepseek/deepseek-v4-flash-0731",
    provider_only: "deepinfra",
    fallback: false,
    retries: 0,
    stream: true,
  },
  caps: { worker_s1_s3: 32000, worker_s4: 64000, selection: 8000,
    compiler: 24000, supplement: 12000, batch_judge: 64000 },
  invalidation: "Use the frozen v9 cap, JSON, transport, identity, and paired-cap invalidation rules. Preserve every invalid attempt and do not replace tasks.",
  staging_rule: "Filename-semantic deterministic staging frozen before outcomes: policy/authority/baseline to S1; negotiation/redlines to S2; risk/financial/legal/business evidence to S3; escalation request/templates to S4. Every source is assigned exactly once.",
  scenarios: index,
}, null, 2)}\n`);

function stage(stage_id, label, release, cold_boundary_before = false) {
  return { stage_id, cold_boundary_before, label, release,
    expected_deliverable: stage_id === "S4" ? "final escalation memo" : `${stage_id.toLowerCase()} evidence-bound analysis` };
}

function classify(file) {
  const value = file.toLowerCase();
  if (/(escalation.*(request|template)|approval-memo-template|memo-template|instructions-to|direction-email)/.test(value)) return "S4";
  if (/(redline|counter|negotiation|revised-draft|negotiated|transmittal)/.test(value)) return "S2";
  if (/(risk|financial|economics|appraisal|valuation|insurance|counsel|business-case|roadmap|benchmark|feasibility|reserves|exposure|availability|portfolio|campaign-spend|schedule|clinical|governance|ipo|guaranty|relationship|syndicate|recommendation)/.test(value)) return "S3";
  return "S1";
}

function outputName(instructions) {
  const match = instructions.match(/### Output:\s*\n([^\n]+)/i);
  if (!match) throw new Error("task instructions do not declare an output filename");
  return match[1].trim();
}
