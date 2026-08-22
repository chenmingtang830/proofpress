import { canonicalJson, sha256 } from "../lib/core.mjs";

const C2_ONLY = Object.freeze(["proofpress/portable-carrier.test-only.json"]);
const CARRIER_KEYS = Object.freeze([
  "admitted_head_sha256",
  "bindings",
  "representation",
  "schema_version",
  "substantive_projection_sha256",
  "test_only",
]);

export function auditInformationParity(c1Files, c2Files) {
  const c1 = toMap(c1Files);
  const c2 = toMap(c2Files);
  const c1Only = [...c1.keys()].filter((item) => !c2.has(item)).sort();
  const c2Only = [...c2.keys()].filter((item) => !c1.has(item)).sort();
  const common = [...c1.keys()].filter((item) => c2.has(item)).sort();
  const byteMismatches = common.filter((item) => !c1.get(item).equals(c2.get(item)));
  const projection = common.map((item) => ({ path: item, sha256: sha256(c1.get(item)) }));
  const projectionSha256 = sha256(canonicalJson(projection));
  const carrierErrors = validateCarrier(c2.get(C2_ONLY[0]), projection, projectionSha256);
  const errors = [];
  if (c1Only.length) errors.push(`C1-only files are not permitted: ${c1Only.join(", ")}`);
  if (JSON.stringify(c2Only) !== JSON.stringify(C2_ONLY)) errors.push(`C2-only paths differ from allowlist: ${c2Only.join(", ")}`);
  if (byteMismatches.length) errors.push(`Common substantive files differ: ${byteMismatches.join(", ")}`);
  errors.push(...carrierErrors);
  return {
    schema_version: 1,
    audit_type: "C1_C2_INFORMATION_PARITY",
    passed: errors.length === 0,
    substantive_projection_sha256: projectionSha256,
    c1_substantive_projection_sha256: projectionSha256,
    c2_substantive_projection_sha256: byteMismatches.length ? null : projectionSha256,
    common_substantive_files: projection,
    allowed_c2_only_files: C2_ONLY,
    observed_c1_only_files: c1Only,
    observed_c2_only_files: c2Only,
    byte_mismatches: byteMismatches,
    errors,
    scope: "Machine equality under the frozen path/hash projection and carrier allowlist; human semantic review remains required before real calls.",
  };
}

export function createTestOnlyCarrier(substantiveFiles) {
  const files = toMap(substantiveFiles);
  const projection = [...files.keys()].sort().map((item) => ({ path: item, sha256: sha256(files.get(item)) }));
  const projectionSha256 = sha256(canonicalJson(projection));
  const handoff = projection.find((item) => item.path === "handoff-state.json");
  if (!handoff) throw new Error("handoff-state.json is required before creating a carrier");
  return Buffer.from(`${JSON.stringify({
    schema_version: "TEST-ONLY/proofpress-portable-mock/v1",
    test_only: true,
    representation: "bindings-only; contains no legal conclusion or recommendation",
    admitted_head_sha256: handoff.sha256,
    substantive_projection_sha256: projectionSha256,
    bindings: projection,
  }, null, 2)}\n`);
}

function validateCarrier(content, projection, projectionSha256) {
  if (!content) return ["C2 portable carrier is missing"];
  let carrier;
  try {
    carrier = JSON.parse(content.toString("utf8"));
  } catch {
    return ["C2 portable carrier is malformed"];
  }
  const errors = [];
  if (JSON.stringify(Object.keys(carrier).sort()) !== JSON.stringify(CARRIER_KEYS)) errors.push("Carrier contains non-allowlisted fields");
  if (carrier.schema_version !== "TEST-ONLY/proofpress-portable-mock/v1" || carrier.test_only !== true) errors.push("Carrier is not labeled TEST-ONLY");
  if (carrier.substantive_projection_sha256 !== projectionSha256) errors.push("Carrier substantive projection hash mismatch");
  if (canonicalJson(carrier.bindings) !== canonicalJson(projection)) errors.push("Carrier bindings differ from substantive projection");
  const handoff = projection.find((item) => item.path === "handoff-state.json");
  if (!handoff || carrier.admitted_head_sha256 !== handoff.sha256) errors.push("Carrier admitted head does not bind handoff-state.json");
  return errors;
}

function toMap(files) {
  const map = new Map();
  for (const file of files) {
    if (!file || typeof file.path !== "string" || !Buffer.isBuffer(file.content)) throw new Error("Parity files require path and Buffer content");
    if (map.has(file.path)) throw new Error(`Duplicate parity path: ${file.path}`);
    map.set(file.path, file.content);
  }
  return map;
}
