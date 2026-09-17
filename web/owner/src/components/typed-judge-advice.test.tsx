import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { expect, it } from "vitest";
import { TypedJudgeAdvice } from "./typed-judge-advice";
import { applyProviderPreset } from "./review-policy";

it("preserves the legacy receipt and identifies typed advice as experimental", () => {
  expect(renderToStaticMarkup(<TypedJudgeAdvice />)).toBe("");
  const html = renderToStaticMarkup(<TypedJudgeAdvice audit={{backend:"jev", requested_model:"jev-latest", response_model:"jev-test", mapping_version:"jev-conservative/v1", latency_ms:10, answers:{recommendation:{type:"choice",confidence:.9,probabilities:{accept:.98,reject:.01,escalate:.01}}}}} />);
  expect(html).toContain("Jev structured advice · experimental");
  expect(html).not.toContain("Approved");
});

it("selects Jev only on an explicit provider change and preserves consent", () => {
  const settings = {provider:"openrouter",model:"saved-model",external_consent:false,mode:"manual"};
  const next = applyProviderPreset(settings,"typesafe",{typesafe:{default_model:"jev-latest"}});
  expect(next).toEqual({...settings,provider:"typesafe",model:"jev-latest",endpoint:""});
  expect(settings.provider).toBe("openrouter");
});
