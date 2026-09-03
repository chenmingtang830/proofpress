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
  it("keeps human admission out of assistant and WebMCP tools", () => {
    expect(source).toContain('name: "get_current_context"');
    expect(source).toContain("Approve is not exposed");
    expect(source).not.toMatch(/name:\s*"(?:approve|admit)/);
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
    expect(source).toContain("Back to review");
  });
});
