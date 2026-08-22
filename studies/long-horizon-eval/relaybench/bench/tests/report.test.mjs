import assert from "node:assert/strict";
import test from "node:test";
import { aggregateRecords } from "../scoring/score.mjs";
import { renderReport } from "../../scripts/bench-report.mjs";

test("report refuses to invent a benchmark result from TEST-ONLY calibration", () => {
  const score = aggregateRecords([{
    test_only:true,
    publishable:false,
    condition:"C1_ORDINARY_PORTABLE",
    stages:[],
    evaluation:{legal_rubric:{status:"NOT_RUN_TEST_ONLY",criteria:[]}},
    invalid:{is_invalid:false,reason:null},
    telemetry:{},
    verifier:{},
  }]);
  const markdown = renderReport(score);
  assert.match(markdown, /No benchmark result/);
  assert.match(markdown, /Excluded TEST-ONLY records: \*\*1\*\*/);
  assert.match(markdown, /Harvey LAB evaluator was not run/);
  assert.doesNotMatch(markdown, /0\.0000|1\.0000/);
});
