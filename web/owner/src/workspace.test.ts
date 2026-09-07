import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const source = readFileSync(
  fileURLToPath(new URL("./main.tsx", import.meta.url)),
  "utf8",
);
const css = readFileSync(
  fileURLToPath(new URL("./index.css", import.meta.url)),
  "utf8",
);
const governanceCss = readFileSync(
  fileURLToPath(new URL("./components/governance.css", import.meta.url)),
  "utf8",
);
const knowledgeSource = readFileSync(fileURLToPath(new URL("./components/knowledge-library.tsx", import.meta.url)), "utf8");

describe("Proofpress owner workspace contract", () => {
  it("keeps the MVP focused on review and human-readable lineage", () => {
    expect(source).not.toContain("Ask Proofpress");
    expect(source).not.toContain("Search claims or IDs");
    expect(source).not.toContain("Inspect receipt");
    expect(source).toContain('"needs_revision"');
    expect(source).toContain('<Button className="reviewEntry" variant="accent" onClick={onOpenFull}>Open full review</Button>');
    expect(source).toContain("Run optional LM review");
    expect(source).toContain("Set up LM review");
    expect(source).toContain("Needs revision");
    expect(source).toContain("View details");
    expect(source).toContain("Technical receipt");
    expect(knowledgeSource).toContain("<LineageGraph");
    expect(source).toContain("(current + 1) * 20");
  });
  it("opens the ledger on current claims and scopes lineage to a selection", () => {
    expect(knowledgeSource).toContain('const [lineage, setLineage] = React.useState(false)');
    expect(knowledgeSource).toContain("Search current claims");
    expect(knowledgeSource).toContain("View lineage");
    expect(knowledgeSource).toContain('receipt?.claim.id === selected');
    expect(source).not.toContain("Show history and unavailable claims");
  });
  it("lets the outer stage scroll the full review surface", () => {
    expect(css).toMatch(/\.inspector\.fullReview\s*\{[^}]*overflow:\s*visible;[^}]*overscroll-behavior:\s*auto;/s);
  });
  it("keeps the full-review entry visible before long LM advice", () => {
    expect(source.indexOf('className="reviewEntry"')).toBeLessThan(source.indexOf('className="lmRationale"'));
    expect(css).toContain("scrollbar-gutter: stable");
    expect(css).toContain("-webkit-line-clamp: 4");
  });
  it("uses progressive disclosure for long review material", () => {
    expect(source).toContain("Read full LM rationale");
    expect(source).toContain('className="revisionDisclosure"');
    expect(source).toContain('label="Show full excerpt"');
    expect(source).toContain("Read the complete advisory rationale in the review summary above.");
    expect(css).toContain(".expandableText p");
  });
  it("explains evidence and downstream consequence before authority changes", () => {
    expect(source).toContain("How claims move through Proofpress");
    expect(source).toContain("Agents propose");
    expect(source).toContain("You decide");
    expect(source).toContain("Approved claims become reusable");
    expect(source).toContain("Evidence for this claim");
    expect(source).toContain("Proposed reuse boundary");
    expect(source).toContain("Available knowledge");
    expect(source).toContain("Needs review");
    expect(source).not.toContain("Outside current context");
    expect(css).toContain("--evidence:");
    expect(css).toContain("--review-queue:");
    expect(css).toContain(".orientation > .reviewOrientation");
    expect(css).toContain(".orientation > .admittedOrientation");
  });

  it("gives first-run and caught-up states an explicit next step", () => {
    expect(source).toContain("No claims yet");
    expect(source).toContain("Manage agent access");
    expect(source).toContain("You are caught up");
    expect(source).toContain("Browse current claims");
    expect(source).toContain("No claims are available for reuse");
    expect(knowledgeSource).toContain("Review candidate claims");
    expect(css).toContain(".claimsPath");
    expect(css).toContain(".emptyState");
  });
  it("delays rejection for ten seconds while continuing the needs-review queue", () => {
    expect(source).toContain('row.state === "needs_review" && row.id !== rejectedId');
    expect(source).toContain('}, 10000)');
    expect(source).toContain('Not recorded yet');
    expect(source).toContain('window.clearTimeout(rejectTimeout.current)');
    expect(source).toContain('>Undo</button>');
    expect(source).toContain('setFullReview(false)');
    expect(css).toContain('.decisionNotice');
  });
  it("continues the review queue after approval and paginates recent decisions", () => {
    expect(source).toContain('decision === "admit"');
    expect(source).toContain("await load(nextPending)");
    expect(source).toContain("const pageSize = 20");
    expect(source).toContain('left.decision_at || left.created_at');
    expect(source).toContain("Page {currentPage + 1} of {pageCount}");
    expect(source).toContain("{pageSize} per page");
  });
  it("uses a concise title and description before the exact claim statement", () => {
    expect(source).toContain("const claimTitle = claimDisplayTitle(r.claim)");
    expect(source).toContain("{claimDisplayTitle(row)}</button>");
    expect(source).toContain('className="claimDescription"');
    expect(source).toContain("Exact claim statement");
    expect(css).toContain(".claimStatementDetails");
  });
  it("keeps escalated LM advice readable and explains why approval is unavailable", () => {
    expect(source).toContain('className="lmRationaleHeader"');
    expect(source).toContain("The LM marked this claim Needs Attention");
    expect(source).toContain("Only Human Approval admits the claim");
    expect(source).toContain(">Refresh LM advice</Button>");
    expect(source).toContain(">Review approval policy</Button>");
    expect(source).not.toContain('r.review_policy?.mode === "manual" && <Button className="secondaryAction"');
    expect(css).toContain(".lmRationale > .expandableText");
    expect(css).not.toContain(".lmRationale > div { display: flex");
  });
  it("keeps human admission out of assistant and WebMCP tools", () => {
    expect(source).toContain('name: "get_current_context"');
    expect(source).toContain("Human Approval is not exposed");
    expect(source).not.toMatch(/name:\s*"(?:approve|admit)/);
  });
  it("makes activity and policy agent-addressable without granting authority", () => {
    expect(source).toContain('name: "get_workspace_summary"');
    expect(source).toContain('name: "list_review_queue"');
    expect(source).toContain('name: "get_activity"');
    expect(source).toContain('name: "run_deterministic_checks"');
    expect(source).toContain('name: "open_review"');
    expect(source).toContain('name: "get_review_policy"');
    expect(source).toContain('name: "prepare_review_policy_change"');
    expect(source).toContain('name: "get_agent_access"');
    expect(source).toContain('name: "prepare_agent_credential_issue"');
    expect(source).toContain("activated: false");
    expect(source).toContain("requires_human_owner: true");
    expect(source).toContain("human_approval_recorded: false");
  });

  it("uses the fixed product name and neutral pending treatment", () => {
    expect(source).toContain("Proofpress");
    expect(source).not.toContain("Proof Press");
    expect(css.toLowerCase()).not.toContain("yellow");
    expect(css.toLowerCase()).not.toContain("gradient");
    expect(css).toContain('--font-ui: "DM Sans"');
    expect(css).toContain('--font-proof: "IBM Plex Mono"');
    expect(`${css}\n${governanceCss}`).not.toMatch(/Georgia|Times New Roman|font-editorial/);
  });

  it("ships desktop and mobile operating layouts", () => {
    expect(css).toContain("grid-template-columns: 226px");
    expect(css).toContain("@media (max-width: 680px)");
    expect(source).toContain("Close details");
    expect(source).toContain('aria-busy="true"');
    expect(source).toContain('pending={!!selected && !receipt}');
  });
  it("keeps review claims readable at compact desktop widths", () => {
    expect(source).toContain('className="tableWrap reviewTableWrap"');
    expect(source).toContain('className="reviewTable"');
    expect(source).toContain('className="reviewScopeCell"');
    expect(css).toMatch(/\.reviewTable \.claimSelect\s*\{[^}]*text-align:\s*left;/s);
    expect(css).toContain("@media (min-width: 681px) and (max-width: 1050px)");
    expect(css).toMatch(/\.reviewTable th:nth-child\(3\),\s*\.reviewTable td\.reviewScopeCell\s*\{\s*display:\s*none;/s);
    expect(css).toMatch(/\.reviewTable td\.reviewScopeCell\s*\{\s*display:\s*none;/s);
    expect(css).toMatch(/\.reviewTable \.claimScopeInline\s*\{\s*display:\s*none;/s);
  });
  it("uses proof typography only for evidence metadata", () => {
    expect(source).toContain('className={`compactEvidenceExcerpt${open ? " expanded" : ""}`}');
    expect(source).toContain('<EvidencePreview row={e} />');
    expect(source).not.toContain('className="blockedAction"');
    expect(source).not.toContain('<span>Source {String(i + 1).padStart(2, "0")}</span>');
    expect(css).toMatch(/\.lmRationale > \.lmRationaleHeader > span\s*\{[^}]*var\(--font-ui\)/s);
    expect(css).toMatch(/\.compactEvidenceExcerpt p\s*\{[^}]*-webkit-line-clamp:\s*3;/s);
    expect(css).toMatch(/\.evidenceArgument\s*\{[^}]*margin:\s*28px 0 22px;[^}]*border:\s*1px solid var\(--line\);/s);
    expect(source).toContain('<section className="reuseBoundary" aria-label="Proposed reuse boundary">');
    expect(css).toMatch(/\.reuseBoundary\s*\{[^}]*margin:\s*20px 0 22px;[^}]*padding:\s*20px 0 0;/s);
  });
});
