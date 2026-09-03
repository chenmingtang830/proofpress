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
  it("keeps human admission out of assistant and WebMCP tools", () => {
    expect(source).toContain('name: "get_current_context"');
    expect(source).toContain("Approve is not exposed");
    expect(source).not.toMatch(/name:\s*"(?:approve|admit)/);
  });
  it("makes activity and policy agent-addressable without granting authority", () => {
    expect(source).toContain('name: "get_activity"');
    expect(source).toContain('name: "get_review_policy"');
    expect(source).toContain('name: "prepare_review_policy_change"');
    expect(source).toContain("activated: false");
    expect(source).toContain("requires_human_owner: true");
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
