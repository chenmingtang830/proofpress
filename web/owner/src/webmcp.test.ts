import { afterEach, describe, expect, it, vi } from "vitest";
import { createOwnerTools } from "./webmcp";

const capture = {purpose:"Preserve bounded test findings.", capture:["One result with evidence and limits."], exclude:["Secrets"]};
const policy = {provider:"managed_gmi",endpoint:"",model:"model",criteria:"Evidence and scope required",zdr:true,mode:"off",require_judge:false,external_consent:false,auto_admit_new_claims:false};
function fixture(api = vi.fn(async (_path: string, _options?: any): Promise<any> => ({}))) {
  const storage = new Map<string,string>();
  vi.stubGlobal("sessionStorage", {setItem:vi.fn((key:string,value:string)=>storage.set(key,value))});
  vi.stubGlobal("location", {origin:"https://example.invalid"});
  vi.stubGlobal("window", {dispatchEvent:vi.fn()});
  const effects = Object.fromEntries(["setSelected","setNote","setReceipt","setPage","setFullReview","setReloadVersion","setAdminSection","navigate"].map(key=>[key,vi.fn()]));
  const tools = createOwnerTools({api,csrfRef:{current:"synthetic-csrf"},selectionRequest:{current:0},...effects});
  const call = async (name:string, input:any = {}) => {
    const response = await tools.find(tool=>tool.name===name)!.execute(input);
    return {response, value:JSON.parse(response.content[0].text)};
  };
  return {api,tools,storage,effects,call};
}
afterEach(()=>vi.unstubAllGlobals());

describe("owner WebMCP behavior", () => {
  it("returns partial summary with unknown counts when policy has not been saved", async () => {
    const missing=Object.assign(new Error("Confirm review policy first"),{code:"workspace_policy_missing"});
    const f=fixture(vi.fn(async path=>{if(path.endsWith("/summary")) return {pending:2};throw missing;}));
    const {response,value}=await f.call("get_workspace_summary");
    expect(response.isError).not.toBe(true);
    expect(value.partial).toBe(true);
    expect(value.review.pending).toBe(2);
    expect(value.current_governed_context_count).toBeNull();
    expect(value.claim_states).toBeNull();
    expect(value.unavailable).toHaveLength(2);
    expect(value.unavailable[0].code).toBe("workspace_policy_missing");
  });
  it("returns structured actionable errors instead of throwing browser UnknownError", async () => {
    const f=fixture(vi.fn(async ()=>{throw new Error("Session expired");}));
    const {response,value}=await f.call("get_capture_policy");
    expect(response.isError).toBe(true);
    expect(value.error.message).toBe("Session expired");
  });
  it("reads capture guidance and prepares validated rules without server writes", async () => {
    const f=fixture(vi.fn(async ()=>({version:3,settings:capture})));
    expect((await f.call("get_capture_policy")).value.version).toBe(3);
    const {value}=await f.call("prepare_capture_policy_change",capture);
    expect(value).toMatchObject({prepared:true,activated:false,requires_human_owner:true});
    expect(JSON.parse(f.storage.get("proofpress:capture-policy-draft")!)).toEqual(capture);
    expect(f.effects.setAdminSection).toHaveBeenCalledWith("rules");
    expect(f.effects.navigate).toHaveBeenCalledWith("admin","?section=rules");
    expect(f.api.mock.calls).toEqual([["/owner/api/capture-policy"]]);
    expect(window.dispatchEvent).toHaveBeenCalled();
  });
  it.each([{...capture,api_key:"never-store"},{...capture,capture:[]},{...capture,capture:["x".repeat(501)]}])("rejects invalid capture drafts without changing storage", async settings=>{
    const f=fixture();
    expect((await f.call("prepare_capture_policy_change",settings)).response.isError).toBe(true);
    expect(f.storage.size).toBe(0);
    expect(f.api).not.toHaveBeenCalled();
    expect(f.effects.navigate).not.toHaveBeenCalled();
  });
  it.each(["managed_gmi","openai_decisions","future_provider"])("uses live provider IDs, including %s, without saving consent or policy", async provider=>{
    const f=fixture(vi.fn(async ()=>({providers:{[provider]:{}}})));
    const result=await f.call("prepare_review_policy_change",{...policy,provider});
    expect(result.value.activated).toBe(false);
    expect(result.value.next).toContain("No provider key or external processing consent is needed while AI is off.");
    expect(JSON.parse(f.storage.get("proofpress:review-policy-draft")!).provider).toBe(provider);
    expect(f.api.mock.calls).toEqual([["/owner/api/review-policy"]]);
  });
  it("rejects unknown provider and credential fields without storing them", async ()=>{
    const f=fixture(vi.fn(async ()=>({providers:{managed_gmi:{}}})));
    expect((await f.call("prepare_review_policy_change",{...policy,provider:"unknown"})).response.isError).toBe(true);
    expect((await f.call("prepare_review_policy_change",{...policy,api_key:"never-store"})).response.isError).toBe(true);
    expect(f.storage.size).toBe(0);
  });
  it.each([{...policy,external_consent:"yes"},{...policy,mode:"enabled"},{...policy,criteria:"x".repeat(8001)}])("validates review draft fields before staging", async settings=>{
    const f=fixture(vi.fn(async ()=>({providers:{managed_gmi:{}}})));
    expect((await f.call("prepare_review_policy_change",settings)).response.isError).toBe(true);
    expect(f.storage.size).toBe(0);
    expect(f.effects.navigate).not.toHaveBeenCalled();
  });
  it("projects identity and credential metadata without returning secrets", async ()=>{
    const f=fixture(vi.fn(async path=>path.endsWith("session")?{workspace_id:"workspace:test",principal:"human:test",role:"owner",csrf:"do-not-return"}:{credentials:[{credential_id:"credential:test",principal_id:"agent:test",role:"agent",token:"do-not-return"}]}));
    expect((await f.call("get_workspace_identity")).value).toEqual({workspace_id:"workspace:test",principal:"human:test",role:"owner"});
    expect((await f.call("get_agent_access")).value.credentials[0]).toEqual({credential_id:"credential:test",principal_id:"agent:test",role:"agent"});
  });
  it("keeps every read tool on GET and every prepare tool free of server mutations", async ()=>{
    const f=fixture(vi.fn(async path=>path.includes("claims/")?{state:"admitted"}:path.endsWith("review-policy")?{providers:{managed_gmi:{}}}:{}));
    for(const tool of f.tools.filter(tool=>tool.annotations?.readOnlyHint)) {
      const result=await tool.execute({claim_id:"claim:test",run_id:"run:test",scope:"project:test",action:"withdraw"});
      expect(result.isError,tool.name).not.toBe(true);
    }
    await f.call("prepare_review_response",{claim_id:"claim:test",response:"Need bounded evidence"});
    await f.call("prepare_review_policy_change",policy);
    await f.call("prepare_capture_policy_change",capture);
    await f.call("prepare_agent_credential_issue",{principal_id:"agent:test",label:"Synthetic"});
    expect(f.api.mock.calls.every(([,options])=>!options?.method || options.method==="GET")).toBe(true);
    expect(f.tools.some(tool=>/^(approve|admit|save|activate|issue|revoke|withdraw|reassess)(_|$)/.test(tool.name))).toBe(false);
  });
});
