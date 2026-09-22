const results: Record<string, {label:string; tone:string}> = {
  ok: {label:"Recorded", tone:"neutral"},
  operation_forbidden: {label:"Access denied", tone:"danger"},
  ledger_head_conflict: {label:"Version conflict", tone:"attention"},
  idempotency_conflict: {label:"Duplicate conflict", tone:"attention"},
  operation_rejected: {label:"Request rejected", tone:"danger"},
  resource_not_found: {label:"Not found", tone:"danger"},
  operation_io_error: {label:"Service error", tone:"danger"},
  judge_failed: {label:"Model review failed", tone:"danger"},
  judge_blocked: {label:"Model review blocked", tone:"danger"},
  judge_interrupted: {label:"Model review interrupted", tone:"danger"},
  judge_skipped: {label:"Model review skipped", tone:"neutral"},
};
export function activityResult(outcome:string) {
  return results[outcome] || {label:outcome ? "Request failed" : "Unknown", tone:outcome ? "danger" : "neutral"};
}
export function ActivityResult({outcome}:{outcome:string}) {
  const result = activityResult(outcome);
  return <span className="activityResult" data-tone={result.tone} title={outcome || "No outcome recorded"}>{result.label}{outcome && outcome !== "ok" && <small>{outcome}</small>}</span>;
}
