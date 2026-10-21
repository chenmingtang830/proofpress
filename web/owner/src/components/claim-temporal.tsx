import { claimTime, type ClaimDisplayRecord } from "./claim-display";

export function ClaimTemporal({claim, compact = false}: {claim: ClaimDisplayRecord; compact?: boolean}) {
  const t = claimTime(claim);
  if (!t.effective && !t.report && !t.known) return null;
  return <span className="claimTemporal" aria-label="Finding dates">
    {t.effective && <span>Data as of <time dateTime={t.effective}>{t.effective.slice(0, 10)}</time></span>}
    {t.report && t.report !== t.effective && (!compact || !t.effective) && <span>Report <time dateTime={t.report}>{t.report.slice(0, 10)}</time></span>}
    {!compact && t.known && <span>First known <time dateTime={t.known}>{t.known}</time></span>}
    {!compact && t.reconstruction && <span>Historical reconstruction{!t.known ? " · first-known time unverified" : ""}</span>}
  </span>;
}
