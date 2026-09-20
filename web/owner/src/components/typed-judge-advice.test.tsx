import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { expect, it, vi } from "vitest";
import { TypedJudgeAdvice } from "./typed-judge-advice";
import { RelationAdvicePanel } from "./relation-advice";
import { applyProviderPreset } from "./review-policy";

vi.mock("./ui/accordion", () => ({
  Accordion: ({children}: {children: React.ReactNode}) => <div>{children}</div>,
  AccordionItem: ({children}: {children: React.ReactNode}) => <div>{children}</div>,
  AccordionContent: ({children}: {children: React.ReactNode}) => <div>{children}</div>,
  AccordionTrigger: ({children}: {children: React.ReactNode}) => <button>{children}</button>,
}));

it("preserves the legacy receipt and identifies typed advice as experimental", () => {
  expect(renderToStaticMarkup(<TypedJudgeAdvice />)).toBe("");
  const html = renderToStaticMarkup(<TypedJudgeAdvice audit={{backend:"jev", requested_model:"jev-latest", response_model:"jev-test", mapping_version:"jev-conservative/v1", latency_ms:10, answers:{recommendation:{type:"choice",confidence:.9,probabilities:{accept:.98,reject:.01,escalate:.01}}}}} />);
  expect(html).toContain("Jev review details · experimental");
  expect(html).not.toContain("Approved");
});

it("shows citation relation advice without presenting it as admission", () => {
  const html = renderToStaticMarkup(<TypedJudgeAdvice audit={{backend:"jev", requested_model:"jev-latest", response_model:"jev-test", mapping_version:"jev-relation-types/v1", latency_ms:10, declared_relation_type:"qualifies", answers:{recommendation:{type:"choice",confidence:.9,probabilities:{accept:.98,reject:.01,escalate:.01}},relation_type:{type:"choice",choice:"supports",confidence:.9,probabilities:{supports:.98,qualifies:.01,contradicts:.01}}}}} />);
  expect(html).toContain("Citation relation classification");
  expect(html).toContain("Declared by proposal");
  expect(html).toContain("Jev primary relation");
  expect(html).toContain("bounded citation advice");
  expect(html).not.toContain("Automatically changed");
});

it("surfaces relation advice from the claim receipt without implying admission", () => {
  const audit = {backend:"jev", requested_model:"jev-latest", response_model:"jev-test", mapping_version:"jev-relation-types/v1", latency_ms:10, declared_relation_type:"qualifies", answers:{recommendation:{type:"choice",confidence:.9,probabilities:{accept:.98,reject:.01,escalate:.01}},relation_type:{type:"choice",choice:"supports",confidence:.9,probabilities:{supports:.98,qualifies:.01,contradicts:.01}}}};
  const html = renderToStaticMarkup(<RelationAdvicePanel items={[{relation:{id:"rel_1",from:"c1",to:"c2",type:"qualifies"},state:"needs_review",recommendation:{recommendation:"escalate",rationale:"The citation supports a different relation.",decision_audit:audit}}]} />);
  expect(html).toContain("Citation relation advice");
  expect(html).toContain("rel_1");
  expect(html).toContain("The citation supports a different relation.");
  expect(html).not.toContain("Automatically changed");
});

it("selects Jev only on an explicit provider change and preserves consent", () => {
  const settings = {provider:"openrouter",model:"saved-model",external_consent:false,mode:"manual"};
  const next = applyProviderPreset(settings,"typesafe",{typesafe:{default_model:"jev-latest"}});
  expect(next).toEqual({...settings,provider:"typesafe",model:"jev-latest",endpoint:""});
  expect(settings.provider).toBe("openrouter");
});
