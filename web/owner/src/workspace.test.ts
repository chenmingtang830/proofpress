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

describe("Proofpress owner workspace contract", () => {
  it("keeps the MVP focused on review and human-readable lineage", () => {
    expect(source).not.toContain("Ask Proofpress");
    expect(source).not.toContain("Search conclusions or IDs");
    expect(source).not.toContain("Inspect receipt");
    expect(source).toContain('"needs_revision"');
    expect(source).toContain("Open full review");
    expect(source).toContain("Needs revision");
    expect(source).toContain("View details");
    expect(source).toContain("Technical receipt");
    expect(source).toContain("Evidence to governed knowledge");
    expect(source).toContain("(current + 1) * 20");
  });
  it("opens the ledger on current knowledge and scopes lineage to a selection", () => {
    expect(source).toContain('const [view, setView] = React.useState("list")');
    expect(source).toContain("Selected lineage");
    expect(source).toContain("View lineage");
    expect(source).not.toContain("Show history and unavailable conclusions");
  });
  it("explains evidence and downstream consequence before authority changes", () => {
    expect(source).toContain("Evidence for this conclusion");
    expect(source).toContain("Proposed reuse boundary");
    expect(source).toContain("Available now");
    expect(source).toContain("Outside current context");
    expect(css).toContain("--evidence:");
    expect(css).toContain("--withheld:");
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
  });

  it("ships desktop and mobile operating layouts", () => {
    expect(css).toContain("grid-template-columns: 226px");
    expect(css).toContain("@media (max-width: 680px)");
    expect(source).toContain("Close details");
    expect(source).toContain('aria-busy="true"');
    expect(source).toContain('pending={!!selected && !receipt}');
  });
});
