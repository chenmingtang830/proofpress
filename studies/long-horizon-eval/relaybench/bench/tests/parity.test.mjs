import assert from "node:assert/strict";
import test from "node:test";
import { auditInformationParity, createTestOnlyCarrier } from "../parity/information-parity.mjs";

function substantive() {
  return [
    {path:"handoff-state.json",content:Buffer.from('{"state":"same"}\n')},
    {path:"releases/S1.json",content:Buffer.from('{"stage":"S1"}\n')},
  ];
}

test("parity passes only for identical substance plus the bindings-only C2 carrier", () => {
  const c1 = substantive();
  const c2 = [...substantive(), {path:"proofpress/portable-carrier.test-only.json",content:createTestOnlyCarrier(c1)}];
  const audit = auditInformationParity(c1, c2);
  assert.equal(audit.passed, true);
  assert.equal(audit.c1_substantive_projection_sha256, audit.c2_substantive_projection_sha256);
  assert.deepEqual(audit.observed_c2_only_files, ["proofpress/portable-carrier.test-only.json"]);
});

test("parity rejects changed substance or unallowlisted C2 information", () => {
  const c1 = substantive();
  const changed = substantive();
  changed[1] = {path:"releases/S1.json",content:Buffer.from('{"stage":"DIFFERENT"}\n')};
  const c2Changed = [...changed, {path:"proofpress/portable-carrier.test-only.json",content:createTestOnlyCarrier(changed)}];
  assert.equal(auditInformationParity(c1, c2Changed).passed, false);

  const c2Extra = [...substantive(),
    {path:"proofpress/portable-carrier.test-only.json",content:createTestOnlyCarrier(c1)},
    {path:"proofpress/legal-recommendation.txt",content:Buffer.from("accept the term")},
  ];
  assert.equal(auditInformationParity(c1, c2Extra).passed, false);
});
