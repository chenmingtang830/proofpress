export type ClaimDisplayRecord = {
  title?: string | null;
  qualifiers?: Record<string, unknown> | null;
  temporal?: Record<string, unknown> | null;
  statement?: string | null;
  label?: string | null;
  applicability?: { title?: string | null } | null;
};

function present(value: string | null | undefined) {
  return typeof value === "string" && value.trim() ? value.trim() : "";
}

/**
 * Prefer the authored claim title. Historical claims created before titles were
 * required may use their recorded applicability title as a concise heading.
 */
export function claimDisplayTitle(claim: ClaimDisplayRecord) {
  const title = present(claim.title)
    || present(claim.applicability?.title)
    || present(claim.statement)
    || present(claim.label)
    || "Untitled claim";
  return compactDatedTitle(title, claim);
}

export function claimStatement(claim: ClaimDisplayRecord) {
  return present(claim.statement) || present(claim.label);
}

export function hasDistinctClaimHeading(claim: ClaimDisplayRecord) {
  const statement = claimStatement(claim);
  return Boolean(statement) && claimDisplayTitle(claim) !== statement;
}

export function claimTime(claim: ClaimDisplayRecord) {
  const q = claim.temporal || claim.qualifiers || {};
  const date = (v: unknown) => typeof v === "string" && /^\d{4}-\d{2}-\d{2}(?:T.*)?$/.test(v) && Number.isFinite(Date.parse(v)) ? v : "";
  return {effective: date(q.effective_date), report: date(q.report_date), known: date(q.original_first_seen_at), reconstruction: q.historical_reconstruction === true};
}

// Compact only redundant date wrappers backed by metadata. Never remove ranges
// or dates inside a substantive comparison, nor change the recorded statement.
function compactDatedTitle(title: string, claim: ClaimDisplayRecord) {
  if (!present(claim.title) && !present(claim.applicability?.title)) return title;
  const t = claimTime(claim);
  let compact = title;
  for (const value of new Set([t.effective, t.report].filter(Boolean))) {
    const day = new Date(value.slice(0, 10) + "T00:00:00Z").toLocaleDateString("en-US", {month: "long", day: "numeric", timeZone: "UTC"});
    compact = compact.replace(new RegExp(`^${day} (?=[A-Za-z])`), "");
    compact = compact.replace(new RegExp(` (reported|described) (on ${day}|in ${day} report)$`), "");
  }
  return compact ? compact[0].toUpperCase() + compact.slice(1) : title;
}
