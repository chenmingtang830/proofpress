import {describe, expect, it} from "vitest";
import {captureDraftPrompt, parseCaptureDraft, formatCaptureRules, parseCaptureText} from "./capture-rules";

const settings={purpose:"Market research",capture:["Dated observations"],exclude:["Duplicate findings"]};
describe("agent-drafted capture rules",()=>{
  it("asks for a bounded draft with no authority or secret changes",()=>{
    const prompt=captureDraftPrompt({settings});
    expect(prompt).toContain("Ask up to three focused questions");
    expect(prompt).toContain("I will review and save it");
    expect(prompt).toContain("Do not include secrets or change approval permissions");
    expect(prompt).toContain("## Purpose\n## Capture\n## Leave out");
    expect(prompt).toContain("without JSON or a code block");
  });
  it("accepts plain or fenced JSON without changing its meaning",()=>{
    expect(parseCaptureDraft(JSON.stringify(settings))).toEqual(settings);
    expect(parseCaptureDraft('```json\n'+JSON.stringify(settings)+'\n```')).toEqual(settings);
  });
  it("rejects fields that could hide an authority change",()=>{
    expect(()=>parseCaptureDraft(JSON.stringify({...settings,auto_admit_new_claims:true}))).toThrow("Use only");
    expect(()=>parseCaptureDraft(JSON.stringify({settings}))).toThrow("Use only");
  });
  it("rejects malformed, empty or oversized rules",()=>{
    for(const value of [null,[],{...settings,capture:[]},{...settings,capture:"anything"},{...settings,exclude:[" "]},{...settings,purpose:"x".repeat(1001)}]){
      expect(()=>parseCaptureDraft(JSON.stringify(value))).toThrow();
    }
  });
});

describe("readable capture rules",()=>{
  it("round trips readable rules, including multiline rules and empty exclusions",()=>{
    for(const value of [settings,{...settings,capture:["A conditional observation\nwith its limits"],exclude:[]}]){
      expect(parseCaptureText(formatCaptureRules(value))).toEqual(value);
    }
  });
  it("keeps legacy JSON paste compatible and rejects authority fields",()=>{
    expect(parseCaptureText(JSON.stringify(settings))).toEqual(settings);
    expect(()=>parseCaptureText(JSON.stringify({...settings,require_judge:false}))).toThrow("Use only");
  });
  it("rejects incomplete, duplicate or unbounded text before saving",()=>{
    for(const value of ["Just some text",formatCaptureRules(settings)+"\n## Capture\n- Extra",formatCaptureRules({...settings,capture:[]}),formatCaptureRules({...settings,exclude:["x".repeat(501)]})]){
      expect(()=>parseCaptureText(value)).toThrow();
    }
  });
});
