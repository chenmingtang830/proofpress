import { describe, expect, it } from "vitest";
import { sourceFilename } from "./evidence-source";

const source = (uri: string) => ({retrieval_receipt: {source: {uri}}});

describe("recorded source filenames", () => {
  it("does not invent a filename from a website origin or query", () => {
    for (const uri of ["https://example.com", "https://www.sec.gov", "https://example.com/?file=report.pdf", "//example.com"]) {
      expect(sourceFilename(source(uri))).toBeNull();
    }
  });
  it("uses the URL pathname or an actual file path", () => {
    expect(sourceFilename(source("https://example.com/research/daily%20report.md?version=2#section"))).toBe("daily report.md");
    expect(sourceFilename(source("reports/prices.xlsx"))).toBe("prices.xlsx");
    expect(sourceFilename(source("file:///research/report.pdf"))).toBe("report.pdf");
  });
  it("keeps an opaque URI unlabeled and uses separately recorded details", () => {
    const row = source("urn:source:" + "a".repeat(64));
    expect(sourceFilename(row)).toBeNull();
    expect(sourceFilename(row, {details: {filename: "daily report.md", location: "Appendix", fields: []}})).toBe("daily report.md");
  });
  it("does not decode a path separator into a filename", () => {
    expect(sourceFilename(source("https://example.com/reports%2Fsecret.md"))).toBeNull();
  });
});
