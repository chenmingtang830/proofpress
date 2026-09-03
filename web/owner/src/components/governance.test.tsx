import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { DecisionNotice, historyActor, revisionInstructions } from "./review-feedback";
import { LineageGraph } from "./lineage-graph";
import { Icon } from "./ui/icon";

describe("governance components", () => {
  it("does not color a revision request as rejection", () => {
    const html = renderToStaticMarkup(<LineageGraph receipt={{conclusion:{id:"r",statement:"Revise units",scope:"test"},state:"needs_revision",evidence:[]}} available={false} evidenceNames={[]} selection="conclusion" onSelect={()=>{}} />);
    expect(html).toContain('class="graphNode revision"');
    expect(html).toContain('class="revision"');
    expect(html).not.toContain('class="graphNode excluded"');
  });
  it("renders locally bundled Hugeicons with a consistent stroke", () => {
    const html = renderToStaticMarkup(<Icon name="home" />);
    expect(html).toContain('<svg');
    expect(html).toContain('stroke-width="1.6"');
    expect(html).toContain('aria-hidden="true"');
    expect(html).not.toContain('<img');
  });
  it("does not invent historical actors", () => {
    expect(historyActor({})).toBe("Actor not recorded");
    expect(historyActor({conclusion:{proposer:"agent:codex"}})).toBe("agent:codex");
    expect(historyActor({verifier:"verifier:deterministic"})).toBe("verifier:deterministic");
    expect(historyActor({judge:"judge:review",model:"test-model"})).toBe("judge:review · test-model");
    expect(historyActor({reviewer:"owner:richard"})).toBe("owner:richard");
  });
  it("uses one notice surface across decision states", () => {
    for (const state of ["admitted","rejected","needs_revision"]) {
      expect(renderToStaticMarkup(<DecisionNotice state={state} />)).toContain('class="decisionNotice"');
    }
  });
  it("binds handoff instructions to a recorded request", () => {
    expect(revisionInstructions({})).toBe("");
    expect(revisionInstructions({conclusion:{id:"knw_a"},review:{note:"Fix units"},revision_request:{event_id:"evt_b"}})).toContain('"revision_request_ref":"evt_b"');
  });
  it("bounds graph disclosure and does not equate admission with eligibility", () => {
    const html = renderToStaticMarkup(<LineageGraph receipt={{conclusion:{id:"a",statement:"Finding",scope:"test"},state:"admitted",evidence:[{},{},{},{}]}} available={false} evidenceNames={["A","B","C","D"]} selection="conclusion" onSelect={()=>{}} />);
    expect(html).toContain("Not eligible in this view");
    expect(html).toContain("Show 1 more sources");
    expect(html).not.toContain("Available for reuse");
  });
});
