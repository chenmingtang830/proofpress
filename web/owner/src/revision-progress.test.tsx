import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { RevisionProgress } from "./components/review-feedback";
const receipt = {claim: {id:"clm_test"}, review:{note:"Narrow the claim"}, revision_request:{event_id:"request_test"}};
const render = (job:any) => renderToStaticMarkup(<RevisionProgress receipt={{...receipt, revision_job:job}} onChoose={()=>{}} />);
describe("request changes journey", () => {
  it("shows progress without making the user copy instructions", () => {
    const html = render({state:"running", detail:"Preparing revision"});
    expect(html).toContain("Preparing revised claim");
    expect(html).not.toContain("Copy instructions");
    expect(html).toContain("needs your approval");
  });
  it("offers the newly proposed claim for review", () => {
    const html = render({state:"completed", detail:"Ready", successor_id:"clm_new"});
    expect(html).toContain("Review revised claim");
    expect(html).not.toContain("Copy instructions");
  });
  it("explains missing evidence and offers an explicit fallback", () => {
    const html = render({state:"needs_evidence", detail:"Supply later prices"});
    expect(html).toContain("More evidence needed");
    expect(html).toContain("Supply later prices");
    expect(html).toContain("Copy instructions for agent");
  });
});
