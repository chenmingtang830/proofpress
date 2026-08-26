import assert from "node:assert/strict";
import test from "node:test";
import { blindMemos, parseTrustStress } from "../evaluation/trust-stress.mjs";

test("trust stress evaluator uses digest-sorted blind ids and preserves inconclusive outcomes", () => {
  const blinded = blindMemos({ C1: "unsafe memo", C2: "safe memo" });
  assert.deepEqual(blinded.map((x) => x.blind_id), ["MEMO_1", "MEMO_2"]);
  const raw = JSON.stringify({ results: blinded.map((x, index) => ({ blind_id: x.blind_id,
    disposition: index ? "inconclusive" : "unsafe", unsafe_claim_propagated: index ? null : true,
    conflict_recognized: index ? null : false, revalidation_or_escalation_preserved: index ? null : false,
    rationale: "bounded", supporting_quotes: [] })) });
  const parsed = parseTrustStress(raw, blinded);
  assert.equal(Object.keys(parsed).length, 2);
  assert.ok(Object.values(parsed).some((x) => x.disposition === "inconclusive"));
});
