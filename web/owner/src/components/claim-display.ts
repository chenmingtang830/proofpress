export type ClaimDisplayRecord = {
  title?: string | null;
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
  return present(claim.title)
    || present(claim.applicability?.title)
    || present(claim.statement)
    || present(claim.label)
    || "Untitled claim";
}

export function claimStatement(claim: ClaimDisplayRecord) {
  return present(claim.statement) || present(claim.label);
}

export function hasDistinctClaimHeading(claim: ClaimDisplayRecord) {
  const statement = claimStatement(claim);
  return Boolean(statement) && claimDisplayTitle(claim) !== statement;
}
