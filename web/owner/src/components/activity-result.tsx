const results: Record<string, {label:string; tone:string}> = {
  ok: {label:"Recorded", tone:"neutral"},
  operation_forbidden: {label:"Access denied", tone:"danger"},
  ledger_head_conflict: {label:"Version conflict", tone:"attention"},
  idempotency_conflict: {label:"Duplicate conflict", tone:"attention"},
  operation_rejected: {label:"Request rejected", tone:"danger"},
  resource_not_found: {label:"Not found", tone:"danger"},
  operation_io_error: {label:"Service error", tone:"danger"},
};
export function activityResult(outcome:string) {
  return results[outcome] || {label:outcome ? "Request failed" : "Unknown", tone:outcome ? "danger" : "neutral"};
}
export function ActivityResult({outcome}:{outcome:string}) {
  const result = activityResult(outcome);
  return <span className="activityResult" data-tone={result.tone} title={outcome || "No outcome recorded"}>{result.label}{outcome && outcome !== "ok" && <small>{outcome}</small>}</span>;
}
