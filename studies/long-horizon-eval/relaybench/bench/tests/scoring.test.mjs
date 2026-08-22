import assert from "node:assert/strict";
import fs from "node:fs";
import test from "node:test";
import { aggregateRecords, scoreRecord } from "../scoring/score.mjs";

test("scorer loads the frozen TEST-ONLY oracle rather than duplicating it", () => {
  const oracle = JSON.parse(fs.readFileSync(
    new URL("../fixtures/h4-msa-escalation-candidate/test-double/scoring-oracle.json", import.meta.url),
    "utf8",
  ));
  assert.equal(oracle.test_only, true);
  assert.equal(oracle.operative_version, "v4");
  assert.equal(Object.keys(oracle.dispositions).length, 4);
});

function episode({testOnly=false,condition="C1_ORDINARY_PORTABLE",legal=[true,true],issues={}} = {}) {
  const expected = {
    indemnity_cap:{disposition:"ESCALATE"},
    data_rights:{disposition:"REJECT",reopened:true},
    termination_fee:{disposition:"NEGOTIATE"},
    audit_rights:{disposition:"ACCEPT"},
    ...issues,
  };
  return {
    test_only:testOnly,
    publishable:!testOnly,
    condition,
    stages:[{receiver_output:{work_product:{operative_version:"v4",issues:expected,authority_boundary_respected:true}}}],
    evaluation:{legal_rubric:{status:"COMPLETE",criteria:legal.map((passed,index)=>({criterion_id:`C-${index+1}`,passed}))}},
    invalid:{is_invalid:false,reason:null},
    telemetry:{wall_clock_latency_ms:10,input_tokens:20,output_tokens:5,provider_cost_usd:0.01},
    verifier:{duration_ms:condition==="C2_PROOFPRESS"?3:null},
  };
}

test("deterministic scorer separates legal quality and state consistency", () => {
  const score = scoreRecord(episode({legal:[true,false]}));
  assert.deepEqual(score.legal_work_product, {available:true,status:"COMPLETE",passed:1,total:2,all_pass:false});
  assert.equal(score.state_consistency.all_pass, true);
  assert.equal(score.state_consistency.total, 7);
});

test("deterministic scorer detects unsafe propagation without pooling outcomes", () => {
  const record = episode({issues:{data_rights:{disposition:"ACCEPT",reopened:false}}});
  const score = scoreRecord(record);
  assert.equal(score.state_consistency.unsafe_propagation_count, 1);
  assert.equal(score.legal_work_product.all_pass, true);
  const report = aggregateRecords([record]);
  assert.deepEqual(report.metrics.final_all_pass_rate, {numerator:1,denominator:1,rate:1});
  assert.deepEqual(report.metrics.unsafe_state_propagation, {numerator:1,denominator:7,rate:1/7});
  assert.equal(report.metrics.horizon_degradation.available, false);
});

test("TEST-ONLY records are excluded from every aggregate metric", () => {
  const report = aggregateRecords([episode({testOnly:true})]);
  assert.equal(report.publishable_records_seen, 0);
  assert.equal(report.excluded_test_only_records, 1);
  assert.equal(report.metrics.final_all_pass_rate.rate, null);
  assert.equal(report.metrics.state_consistency_criterion_rate.rate, null);
  assert.match(report.note, /No benchmark result/);
});
