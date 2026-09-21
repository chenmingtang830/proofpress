import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { DecisionNotice, historyActor, revisionInstructions } from "./review-feedback";
import { LineageGraph } from "./lineage-graph";
import { ClaimGraph } from "./claim-graph";
import { KnowledgeRecord } from "./knowledge-library";
import { Icon } from "./ui/icon";
import { activityResult } from "./activity-result";
import { Badge } from "./ui/badge";
import { applyProviderPreset, ensureProviderDefault, mergeAgentPolicyDraft, providerModelOptions } from "./review-policy";

describe("governance components", () => {
  it("keeps advisory support visually separate from admission", () => {
    const support=renderToStaticMarkup(<Badge state="accept" />);
    expect(support).toContain("Evidence supported");
    expect(support).not.toContain("--add-bg");
    expect(renderToStaticMarkup(<Badge state="admitted" />)).toContain("--add-bg");
    expect(renderToStaticMarkup(<Badge state="unresolved" />)).toContain("Needs revalidation");
    expect(renderToStaticMarkup(<Badge state="dependency_invalidated" />)).toContain("Dependency changed");
  });
  it("keeps request outcomes distinct from claim admission", () => {
    expect(activityResult("ok")).toEqual({label:"Recorded",tone:"neutral"});
    expect(activityResult("operation_forbidden")).toEqual({label:"Access denied",tone:"danger"});
    expect(activityResult("ledger_head_conflict")).toEqual({label:"Version conflict",tone:"attention"});
    expect(activityResult("unknown_error").label).toBe("Request failed");
  });
  it("does not color a revision request as rejection", () => {
    const html = renderToStaticMarkup(<LineageGraph receipt={{claim:{id:"r",statement:"Revise units",scope:"test"},state:"needs_revision",evidence:[]}} available={false} evidenceNames={[]} selection="claim" onSelect={()=>{}} />);
    expect(html).toContain('graphNode claim revision');
    expect(html).toContain('class="revision"');
    expect(html).not.toContain('class="graphNode excluded"');
  });
  it("renders dependency invalidation as a blocked lineage path", () => {
    const html = renderToStaticMarkup(<LineageGraph receipt={{claim:{id:"a",statement:"Dependent",scope:"test"},state:"dependency_invalidated",evidence:[],dependency_impact:{items:[{relation_id:"r",reason:"withdrawn",path:["a","b"]}]}}} available={false} evidenceNames={[]} selection="claim" onSelect={()=>{}} />);
    expect(html).toContain("graphNode claim excluded");
    expect(html).toContain("Why reuse is paused");
    expect(html).toContain("a → depends on b");
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
    expect(historyActor({claim:{proposer:"agent:codex"}})).toBe("agent:codex");
    expect(historyActor({verifier:"verifier:deterministic"})).toBe("verifier:deterministic");
    expect(historyActor({judge:"judge:review",model:"test-model"})).toBe("judge:review · test-model");
    expect(historyActor({reviewer:"owner:richard"})).toBe("owner:richard");
  });
  it("uses one notice surface across decision states", () => {
    for (const state of ["admitted","rejected","needs_revision"]) {
      expect(renderToStaticMarkup(<DecisionNotice state={state} />)).toContain('decisionNotice');
    }
  });
  it("binds handoff instructions to a recorded request", () => {
    expect(revisionInstructions({})).toBe("");
    expect(revisionInstructions({claim:{id:"knw_a"},review:{note:"Fix units"},revision_request:{event_id:"evt_b"}})).toContain('"revision_request_ref":"evt_b"');
  });
  it("bounds graph disclosure and does not equate admission with eligibility", () => {
    const html = renderToStaticMarkup(<LineageGraph receipt={{claim:{id:"a",statement:"Finding",scope:"test"},state:"admitted",evidence:[{},{},{},{}]}} available={false} evidenceNames={["A","B","C","D"]} selection="claim" onSelect={()=>{}} />);
    expect(html).toContain("Not eligible in this view");
    expect(html).toContain("Show 1 more sources");
    expect(html).not.toContain("Available for reuse");
  });
  it("shows citation-bound relation state and keeps Jev advice advisory", () => {
    const rows = [
      {id:"a",label:"Primary finding",applicability:{title:"Matter"}},
      {id:"b",label:"Bounded qualification",applicability:{title:"Matter"}},
    ];
    const html = renderToStaticMarkup(<ClaimGraph rows={rows} nodes={[{id:"ev",label:"Source receipt"}]} edges={[
      {from:"ev",to:"a",type:"supports"},
      {id:"support-rel",from:"b",to:"a",type:"supports",state:"admitted"},
      {id:"rel",from:"b",to:"a",type:"qualifies",state:"admitted",citation:{evidence_ref:"ev"},advice:{recommendation:"accept"}},
    ]} relations={[]} onChoose={()=>{}} />);
    expect(html).toContain("Citation bound");
    expect(html).toContain("Jev: accept");
    expect(html).toContain("model advice remains advisory");
    expect(html).toContain("Claim-centered lineage");
    expect(html).toContain("2 relations");
    expect(html).toContain("<small>Evidence</small><strong>Source receipt</strong>");
    expect(html).not.toContain("<small>Evidence</small><strong>Bounded qualification</strong>");
  });
  it("reports every recorded relation while keeping details collapsed", () => {
    const rows = Array.from({length:6}, (_, index) => ({id:`c${index}`,label:`Claim ${index}`}));
    const relations = Array.from({length:13}, (_, index) => ({
      id:`r${index}`, from:`c${index % 6}`, to:`c${(index + 1) % 6}`, type:"depends_on", state:"admitted",
    }));
    const html = renderToStaticMarkup(<ClaimGraph rows={rows} nodes={rows.map(row => ({...row,type:"claim"}))} edges={relations} relations={[]} onChoose={()=>{}} />);
    expect(html).toContain("13 relations");
    expect(html).not.toContain("claimRelationList");
  });
  it("discloses bounded evidence truncation with an expansion control", () => {
    const row = {id:"claim",label:"Evidence-heavy claim"};
    const nodes = Array.from({length:17}, (_, index) => ({id:`ev${index}`,type:"evidence",label:`Evidence ${index}`}));
    const edges = nodes.map(node => ({from:node.id,to:row.id,type:"supports"}));
    const html = renderToStaticMarkup(<ClaimGraph rows={[row]} nodes={[...nodes,{...row,type:"claim"}]} edges={edges} relations={[]} onChoose={()=>{}} />);
    expect(html).toContain("Showing 16 of 17 evidence receipts");
    expect(html).toContain("Show 1 more evidence");
  });
  it("shows invalidated admitted claims as paused while preserving withdrawal access", () => {
    const html = renderToStaticMarkup(<KnowledgeRecord receipt={{
      state:"dependency_invalidated", ledger_head:"head", claim:{id:"claim",statement:"Paused claim"},
      evidence:[], history:[], dependent_impact:{direct_ids:[],transitive_ids:[]},
    }} available={false} onClose={()=>{}} onLineage={()=>{}} onWithdraw={()=>{}} busy={false} renderEvidence={()=>null} evidenceName={()=>"Evidence"} />);
    expect(html).toContain("Reuse paused");
    expect(html).toContain("excluded from current context until reassessed");
    expect(html).toContain("Withdraw claim");
    expect(html).not.toContain("Current for this owner view");
  });
  it("does not mislabel contradiction exclusion as dependency invalidation", () => {
    const html = renderToStaticMarkup(<KnowledgeRecord receipt={{
      state:"admitted", ledger_head:"head", claim:{id:"claim",statement:"Contradicted claim"},
      evidence:[], history:[], dependent_impact:{direct_ids:[],transitive_ids:[]},
    }} available={false} blockedReason="contradiction_unresolved" onClose={()=>{}} onLineage={()=>{}} onWithdraw={()=>{}} busy={false} renderEvidence={()=>null} evidenceName={()=>"Evidence"} />);
    expect(html).toContain("Human conflict review is required");
    expect(html).not.toContain("A dependency changed");
    expect(html).toContain("Withdraw claim");
  });
  it("loads criteria-only agent drafts without erasing model configuration", () => {
    const current = {provider:"openrouter", model:"deepseek/deepseek-v4-flash", rubric:"evidence-support/v1", criteria:"old", mode:"automatic", require_judge:true, external_consent:true, zdr:true, endpoint:""};
    expect(mergeAgentPolicyDraft(current, {criteria:"Require primary evidence."})).toEqual({...current, criteria:"Require primary evidence."});
    expect(mergeAgentPolicyDraft(current, {policy:{criteria:"Escalate high-stakes claims."}}).criteria).toBe("Escalate high-stakes claims.");
    expect(() => mergeAgentPolicyDraft(current, {unrelated:true})).toThrow();
  });
  it("updates the default model when the provider changes", () => {
    const current = {provider:"openrouter", model:"deepseek/deepseek-v4-flash", endpoint:"https://old.example/v1"};
    const providers = {openai:{default_model:"gpt-5.4"}, custom:{default_model:""}};
    expect(applyProviderPreset(current, "openai", providers)).toEqual({provider:"openai", model:"gpt-5.4", endpoint:""});
    expect(applyProviderPreset(current, "custom", providers)).toEqual({provider:"custom", model:"", endpoint:""});
  });
  it("shows provider models while preserving a saved model outside the current catalog", () => {
    const provider = {models:["gpt-5.4", "gpt-5.4-mini"]};
    expect(providerModelOptions(provider, "gpt-5.4")).toEqual(["gpt-5.4", "gpt-5.4-mini"]);
    expect(providerModelOptions(provider, "legacy-deployment")).toEqual(["legacy-deployment", "gpt-5.4", "gpt-5.4-mini"]);
  });
  it("keeps all ten ranked provider defaults in order", () => {
    const models = Array.from({length:10}, (_, index) => `model-${index}`);
    expect(providerModelOptions({models}, "model-0")).toEqual(models);
  });
  it("initializes a fresh workspace with the selected provider default", () => {
    const settings = {provider:"openrouter", model:"", mode:"automatic"};
    const providers = {openrouter:{default_model:"deepseek/deepseek-v4-flash"}};
    expect(ensureProviderDefault(settings, providers).model).toBe("deepseek/deepseek-v4-flash");
    expect(ensureProviderDefault({...settings, model:"saved-model"}, providers).model).toBe("saved-model");
  });
});
