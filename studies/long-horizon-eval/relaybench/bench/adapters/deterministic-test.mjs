import fs from "node:fs/promises";
import path from "node:path";
import { validateAdapter } from "./adapter-contract.mjs";

export async function createAdapter() {
  return validateAdapter({
    id: "TEST-ONLY/h4-deterministic-state-reducer",
    testOnly: true,
    metadata() {
      return testOnlyMetadata();
    },
    async invoke(request, context) {
      return invokeDeterministicStage({
        workspace: context.workspace,
        stageId: context.stageId,
        verifierEvidence: request.verifier_evidence,
      });
    },
  });
}

export async function invokeDeterministicStage({ workspace, stageId, verifierEvidence }) {
  if (!/^S[1-4]$/.test(stageId)) throw new Error("TEST-ONLY stage ID must be S1 through S4");
  if (stageId === "S3" && verifierEvidence?.required === true && verifierEvidence.status !== "ok") {
    throw new Error("TEST-ONLY C2 receiver refuses to act without ok verifier evidence");
  }
  const releasesDirectory = path.join(workspace, "releases");
  const names = (await fs.readdir(releasesDirectory)).filter((name) => /^S[1-4]\.json$/.test(name)).sort();
  const visibleNames = names.filter((name) => name.slice(0, 2) <= stageId);
  const issues = {};
  let operativeVersion = null;
  for (const name of visibleNames) {
    const release = JSON.parse(await fs.readFile(path.join(releasesDirectory, name), "utf8"));
    if (release.test_only !== true || release.stage_id !== name.slice(0, 2)) throw new Error(`Invalid TEST-ONLY release: ${name}`);
    operativeVersion = release.operative_version;
    for (const update of release.updates) issues[update.issue_id] = { ...issues[update.issue_id], ...update, source_stage: release.stage_id };
  }
  const output = {
    stage_id: stageId,
    test_only: true,
    work_product: {
      operative_version: operativeVersion,
      issues,
      authority_boundary_respected: Object.values(issues).every((issue) =>
        issue.authority !== "EXECUTIVE_APPROVAL_REQUIRED" || issue.disposition === "ESCALATE"),
      note: "Deterministic TEST-ONLY state reduction; no legal reasoning or benchmark result.",
    },
  };
  return {
    raw_output: JSON.stringify(output),
    telemetry: {
      input_tokens: null,
      output_tokens: null,
      provider_cost_usd: null,
      provider_reported: false,
    },
  };
}

export function testOnlyMetadata() {
  return {
    provider: "TEST-ONLY",
    route: "local-child-process",
    resolved_model: "TEST-ONLY/no-model",
    reasoning_effort: "TEST-ONLY",
    temperature: null,
    seed: 0,
    provider_fallback: false,
    cross_provider_retries: false,
  };
}
