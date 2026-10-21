import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { DecisionNotice, RevisionPanel, historyActor, reviewQueue, revisionInstructions } from "./review-feedback";
import { LineageGraph } from "./lineage-graph";
import { ClaimGraph } from "./claim-graph";
import { KnowledgeLibrary, KnowledgeRecord } from "./knowledge-library";
import { Icon } from "./ui/icon";
import { activityResult } from "./activity-result";
import { Badge } from "./ui/badge";
import { settingsForOwnerSave, applyProviderPreset, ensureProviderDefault, mergeAgentPolicyDraft, providerModelOptions, initialProviderSettings, providerCredentialReady } from "./review-policy";

describe("governance components", () => {
  it("defaults only untouched workspaces to hosted verification without opting in", () => {
    const record = {version:0, settings:{provider:"openrouter", model:"", mode:"off", external_consent:false}, credential:{configured:false}, providers:{managed_openai_decisions:{managed:true, available:false, default_model:"gpt-6-luna"}}};
    const selected = initialProviderSettings(record);
    expect(selected.provider).toBe("managed_openai_decisions");
    expect(selected.external_consent).toBe(false);
    expect(selected.mode).toBe("off");
    expect(initialProviderSettings({...record, version:1}).provider).toBe("openrouter");
    expect(initialProviderSettings({...record, credential:{configured:true}}).provider).toBe("openrouter");
    expect(providerCredentialReady(record, selected, "", false)).toBe(false);
    record.providers.managed_openai_decisions.available = true;
    expect(providerCredentialReady(record, selected, "", false)).toBe(true);
    expect(providerCredentialReady({...record, credential:{configured:true, managed:true}}, {provider:"openai_decisions"}, "", false)).toBe(false);
  });
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
  it("moves a change request out of the queue once a later claim answers it", () => {
    expect(reviewQueue("needs_revision")).toBe("needs_revision");
    expect(reviewQueue("needs_revision", "knw_c")).toBe("decided");
    expect(reviewQueue("needs_review", "knw_c")).toBe("needs_review");
    expect(reviewQueue("unresolved")).toBe("needs_review");
    expect(reviewQueue("dependency_invalidated")).toBe("needs_reassessment");
    expect(reviewQueue("blocked")).toBe("needs_correction");
    expect(reviewQueue("admitted")).toBe("decided");
  });
  it("does not hand off a revision that a later claim already answers", () => {
    const sentBack = {claim:{id:"knw_a"},review:{note:"Fix units"},revision_request:{event_id:"evt_b"}};
    const settled = {...sentBack, lineage:{successor_id:"knw_c",successor_state:"admitted",lineage_path:["knw_a","knw_c"]}};
    expect(revisionInstructions(settled)).toBe("");
    const html = renderToStaticMarkup(<RevisionPanel receipt={settled} onChoose={()=>{}} />);
    expect(html).toContain("Settled by an approved claim");
    expect(html).toContain("knw_c");
    expect(html).not.toContain("Copy instructions for agent");
    const later = {...sentBack, lineage:{successor_id:"knw_d",successor_state:"needs_revision",lineage_path:["knw_a","knw_d"]}};
    expect(renderToStaticMarkup(<RevisionPanel receipt={later} onChoose={()=>{}} />)).toContain("A later revision was also sent back");
    expect(renderToStaticMarkup(<RevisionPanel receipt={sentBack} onChoose={()=>{}} />)).toContain("Copy instructions for agent");
    const withheld = renderToStaticMarkup(<RevisionPanel receipt={{...sentBack, lineage:{withheld:true}}} onChoose={()=>{}} />);
    expect(withheld).toContain("Answered by a claim you cannot view");
    expect(withheld).not.toContain("Copy instructions for agent");
    expect(withheld).not.toContain("Open ");
  });
  it("bounds graph disclosure and does not equate admission with eligibility", () => {
    const html = renderToStaticMarkup(<LineageGraph receipt={{claim:{id:"a",statement:"Finding",scope:"test"},state:"admitted",evidence:[{},{},{},{}]}} available={false} evidenceNames={["A","B","C","D"]} selection="claim" onSelect={()=>{}} />);
    expect(html).toContain("Not eligible in this view");
    expect(html).toContain("Show 1 more sources");
    expect(html).not.toContain("Available for reuse");
  });
  it("preserves contradiction exclusion in lineage", () => {
    const html = renderToStaticMarkup(<LineageGraph receipt={{claim:{id:"a",statement:"Finding",scope:"test"},state:"admitted",evidence:[]}} available={false} blockedReason="contradiction_unresolved" evidenceNames={[]} selection="context" onSelect={()=>{}} />);
    expect(html).toContain("Excluded: unresolved contradiction");
    expect(html).toContain("Human conflict review required");
    expect(html).not.toContain("Approved by");
  });
  it("shows citation-bound relation state and attributes model advice to its adapter", () => {
    const rows = [
      {id:"a",label:"Primary finding",applicability:{title:"Matter"}},
      {id:"b",label:"Bounded qualification",applicability:{title:"Matter"}},
    ];
    const html = renderToStaticMarkup(<ClaimGraph rows={rows} nodes={[{id:"ev",label:"Source receipt"}]} edges={[
      {from:"ev",to:"a",type:"supports"},
      {id:"support-rel",from:"b",to:"a",type:"supports",state:"admitted"},
      {id:"rel",from:"b",to:"a",type:"qualifies",state:"admitted",citation:{evidence_ref:"ev"},advice:{recommendation:"accept",adapter:"proofpress-custom-judge/v1",model:"bounded-model"}},
    ]} relations={[]} onChoose={()=>{}} />);
    expect(html).toContain("Citation bound");
    expect(html).toContain("proofpress-custom-judge/v1 · bounded-model: accept");
    expect(html).not.toContain("Jev: accept");
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
  it("opens current knowledge in Map by default", () => {
    const row = {id:"claim",label:"Current claim",state:"admitted"};
    const html = renderToStaticMarkup(<KnowledgeLibrary rows={[row]} allRows={[row]} nodes={[{id:"claim",type:"claim"}]} edges={[]} relations={[]} selected="" receipt={null} onChoose={()=>{}} onReview={()=>{}} loading={false} contextError="" detailError="" renderEvidence={()=>null} evidenceName={()=>"Evidence"} />);
    expect(html).toContain('aria-pressed="true">Map</button>');
    expect(html).toContain("Current claim graph");
    expect(html).not.toContain("knowledgeList");
  });
  it("offers an accessible resize handle and collapse controls when a record is open", () => {
    const row = {id:"claim",label:"Current claim",state:"admitted"};
    const receipt = {state:"admitted",claim:{id:"claim",statement:"Current claim"},evidence:[],history:[]};
    const html = renderToStaticMarkup(<KnowledgeLibrary rows={[row]} allRows={[row]} nodes={[{id:"claim",type:"claim"}]} edges={[]} relations={[]} selected="claim" receipt={receipt} onChoose={()=>{}} onReview={()=>{}} loading={false} contextError="" detailError="" renderEvidence={()=>null} evidenceName={()=>"Evidence"} />);
    expect(html).toContain('role="separator"');
    expect(html).toContain('aria-label="Resize Knowledge panes"');
    expect(html).toContain('aria-label="Collapse map"');
    expect(html).toContain('aria-label="Collapse details"');
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
  it("does not infer exclusion when current context is unavailable", () => {
    const receipt = {state:"admitted",claim:{id:"claim",statement:"Claim"},evidence:[]};
    const html = renderToStaticMarkup(<KnowledgeLibrary rows={[]} allRows={[{id:"claim",label:"Claim",state:"admitted"}]} nodes={[]} edges={[]} relations={[]} blocked={[]} selected="claim" receipt={receipt} onChoose={()=>{}} onReview={()=>{}} loading={false} contextError="Context unavailable" detailError="" renderEvidence={()=>null} evidenceName={()=>"Evidence"} />);
    expect(html).toContain("Record unavailable");
    expect(html).not.toContain("Reuse paused");
    expect(html).not.toContain("Available for reuse");
  });
  it("keeps a failed ledger deep link open with recovery controls", () => {
    const html = renderToStaticMarkup(<KnowledgeLibrary rows={[]} allRows={[]} nodes={[]} edges={[]} relations={[]} blocked={[]} selected="missing-claim" receipt={null} onChoose={()=>{}} onReview={()=>{}} loading={false} contextError="" detailError="Receipt unavailable" renderEvidence={()=>null} evidenceName={()=>"Evidence"} />);
    expect(html).toContain("Record unavailable");
    expect(html).toContain("Retry details");
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

describe("Owner save processing consent", () => {
  it("binds consent to the submitted destination only on save without changing approval authority", () => {
    const draft = {mode:"automatic",provider:"custom",endpoint:"https://example.com/review",external_consent:false,require_judge:false,auto_admit_new_claims:false};
    expect(settingsForOwnerSave(draft)).toEqual({...draft,external_consent:true});
    expect(draft.external_consent).toBe(false);
    expect(settingsForOwnerSave({...draft,mode:"off",external_consent:true}).external_consent).toBe(false);
  });
});
