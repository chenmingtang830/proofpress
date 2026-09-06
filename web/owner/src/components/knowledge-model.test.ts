import { describe, expect, it } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import React from "react";
import { admissionRecord, recordedIdentity, selectKnowledge, type KnowledgeRow } from "./knowledge-model";
import { KnowledgeRecord } from "./knowledge-library";

const rows: KnowledgeRow[] = [
  { id: "a", label: "Alpha deployment contract", state: "admitted", created_at: "2026-09-01", applicability: { title: "Runtime", keywords: ["Python"] } },
  { id: "b", label: "Beta evidence boundary", state: "admitted", created_at: "2026-09-05", applicability: { title: "Research", description: "CPU experiment" } },
  { id: "c", label: "Gamma legacy record", state: "unresolved" },
];
describe("knowledge browsing", () => {
  it("renders recorded actor objects safely without manufacturing identity", () => {
    expect(recordedIdentity({ id: "human:richard", name: "Richard" }, "missing")).toBe("human:richard");
    expect(recordedIdentity({ name: "Richard" }, "missing")).toBe("Richard");
    expect(recordedIdentity({ id: { bad: true } }, "missing")).toBe("missing");
    const html = renderToStaticMarkup(React.createElement(KnowledgeRecord, { receipt: { claim: { id: "c", statement: "Claim", proposer: { id: "agent:a" } }, review: { decision: "admit", reviewer: { name: "Richard" } }, history: [{ type: "model_reviewed", actor: { id: "agent:j" }, model: "model-v1" }] }, renderEvidence: () => null, evidenceName: () => "Evidence", onClose: () => {}, onLineage: () => {} }));
    expect(html).toContain("agent:a"); expect(html).toContain("Richard"); expect(html).toContain("agent:j · model-v1");
  });
  it("searches across recorded fields and combines query terms with applicability", () => {
    expect(selectKnowledge(rows, "alpha PYTHON", "Runtime", "newest").map(row => row.id)).toEqual(["a"]);
    expect(selectKnowledge(rows, "cpu", "Runtime", "newest")).toEqual([]);
  });
  it("sorts dates without mutating the projection and puts missing dates last", () => {
    expect(selectKnowledge(rows, "", "", "newest").map(row => row.id)).toEqual(["b", "a", "c"]);
    expect(selectKnowledge(rows, "", "", "oldest").map(row => row.id)).toEqual(["a", "b", "c"]);
    expect(selectKnowledge(rows, "", "", "statement").map(row => row.id)).toEqual(["a", "b", "c"]);
    expect(rows.map(row => row.id)).toEqual(["a", "b", "c"]);
  });
  it("uses membership in the eligible projection, never a client state inference", () => {
    expect(selectKnowledge(rows, "", "", "newest")).toHaveLength(3);
  });
  it("never uses automated advice or a rejecting reviewer as an authorizer", () => {
    expect(admissionRecord({ review: { decision: "reject", reviewer: "human:x" }, recommendation: { recommendation: "accept", reviewer: "agent:y" } })).toBeNull();
    expect(admissionRecord({ history: [{ type: "human_reviewed", decision: "admit", reviewer: "human:z" }] })?.reviewer).toBe("human:z");
  });
  it("makes missing provenance and limits explicit in a sparse receipt", () => {
    const html = renderToStaticMarkup(React.createElement(KnowledgeRecord, { receipt: { claim: { id: "c", statement: "A bounded claim", evidence_refs: ["ev_1"] } }, renderEvidence: () => null, evidenceName: () => "Evidence", onClose: () => {}, onLineage: () => {} }));
    expect(html).toContain("Proposer not recorded");
    expect(html).toContain("Authorizer not recorded");
    expect(html).toContain("No explicit validity conditions recorded");
    expect(html).toContain("1 evidence references are recorded");
  });
});
