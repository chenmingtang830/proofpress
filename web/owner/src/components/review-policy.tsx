import { Label } from "@/components/ui/label";
import { NativeSelect } from "@/components/ui/native-select";
import { Input } from "@/components/ui/input";
import { DisclosureContent, Disclosure, DisclosureTrigger } from "@/components/ui/disclosure";
import { Checkbox } from "./ui/checkbox";
import { Switch } from "./ui/switch";
import { MarkdownEditor } from "./ui/markdown-editor";
import React from "react";
import { PolicyHistory } from "./policy-history";
import { CheckmarkCircle02Icon } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { Button } from "./ui/button";
import { Check } from "./ui/icon";
import { Card, CardContent, CardDescription, CardHeader } from "./ui/card";

const AGENT_POLICY_FIELDS = ["provider","endpoint","model","criteria","zdr","mode","require_judge","external_consent","auto_admit_new_claims"];

export function mergeAgentPolicyDraft(current: any, draft: any) {
  if (!draft || typeof draft !== "object" || Array.isArray(draft)) throw new Error("invalid draft");
  const source = draft.policy && typeof draft.policy === "object" ? draft.policy : draft;
  const next = {...current};
  let recognized = false;
  for (const key of AGENT_POLICY_FIELDS) {
    if (key in source) { next[key] = source[key]; recognized = true; }
  }
  if (!recognized) throw new Error("invalid draft");
  return next;
}

export function applyProviderPreset(settings: any, provider: string, providers: any) {
  const preset = providers?.[provider] || {};
  return {...settings, provider, model:preset.default_model || "", endpoint:""};
}

export function providerModelOptions(provider: any, current: string) {
  const models = Array.isArray(provider?.models) ? provider.models : [];
  return current && !models.includes(current) ? [current, ...models] : models;
}

export function ensureProviderDefault(settings: any, providers: any) {
  if (settings?.model) return settings;
  const defaultModel = providers?.[settings?.provider]?.default_model || "";
  return {...settings, model:defaultModel};
}

export function initialProviderSettings(record: any) {
  const settings = record.settings;
  // Only an untouched workspace without a saved key gets the hosted preset.
  // Existing provider choices and consent are never migrated or activated.
  if (record.version === 0 && settings.mode === "off" && !record.credential.configured && record.providers?.managed_gmi) {
    return applyProviderPreset(settings, "managed_gmi", record.providers);
  }
  return ensureProviderDefault(settings, record.providers);
}

export function providerCredentialReady(record: any, settings: any, apiKey: string, removeKey: boolean) {
  if (record?.providers?.[settings?.provider]?.managed) return Boolean(record.providers[settings.provider].available);
  return Boolean(apiKey.trim()) || Boolean(record?.settings?.provider === settings?.provider && record?.credential?.configured && !record?.credential?.managed && !removeKey);
}

export function humanReviewSettings(settings: any) {
  return {...settings, mode:"off", require_judge:false, external_consent:false, auto_admit_new_claims:false};
}

// Called only by the Owner form submission, after the provider disclosure is shown.
export function settingsForOwnerSave(settings: any) {
  return {...settings, external_consent:settings.mode !== "off"};
}

export function ReviewPolicy({csrf, api, onSaved, localPreview = false}: any) {
  const [record, setRecord] = React.useState<any>(null);
  const [settings, setSettings] = React.useState<any>(null);
  const [apiKey, setApiKey] = React.useState("");
  const [removeKey, setRemoveKey] = React.useState(false);
  const [busy, setBusy] = React.useState(false);
  const [message, setMessage] = React.useState("");
  const [error, setError] = React.useState("");
  const [criteriaMessage, setCriteriaMessage] = React.useState("");
  const [criteriaError, setCriteriaError] = React.useState("");
  const [copied, setCopied] = React.useState(false);
  const [showAuthoringPrompt, setShowAuthoringPrompt] = React.useState(false);
  const load = React.useCallback(async () => {
    try {
      const row = await api("/owner/api/review-policy");
      setRecord(row);
      const initial = row.version === 0 ? humanReviewSettings(row.settings) : row.settings;
      const base = initialProviderSettings({...row, settings:{...initial, mode:initial.mode === "off" ? "off" : "automatic"}});
      const prepared = sessionStorage.getItem("proofpress:review-policy-draft");
      if (prepared) {
        const parsed = JSON.parse(prepared);
        try {
          const next = mergeAgentPolicyDraft(base, parsed);
          setSettings({...next,mode:next.mode === "off" ? "off" : "automatic"});
          setMessage("Agent-prepared policy loaded. Review every field before activating it.");
          sessionStorage.removeItem("proofpress:review-policy-draft");
        } catch { setSettings(base); }
      } else setSettings(base);
      setError("");
    }
    catch (e:any) { setError(e.message); }
  }, [api]);
  React.useEffect(() => { void load(); }, [load]);
  const settingsReady = Boolean(settings);
  React.useEffect(() => {
    if (!settingsReady) return;
    const loadCriteriaDraft = () => {
      const raw = sessionStorage.getItem("proofpress:review-policy-draft");
      if (!raw) return;
      try {
        const draft = JSON.parse(raw);
        if (typeof draft.criteria !== "string" || draft.criteria.length > 8000) return;
        setSettings((current:any)=>current ? {...current, criteria:draft.criteria} : current);
        setCriteriaMessage(""); setCriteriaError("");
        sessionStorage.removeItem("proofpress:review-policy-draft");
      } catch { /* Leave an invalid draft untouched for its author. */ }
    };
    window.addEventListener("proofpress:review-criteria-draft", loadCriteriaDraft);
    return () => window.removeEventListener("proofpress:review-criteria-draft", loadCriteriaDraft);
  }, [settingsReady]);
  const change = (key:string, value:any) => { setSettings({...settings, [key]:value}); setMessage(""); };
  async function activate(nextSettings: any, useProviderInput = true) {
    setBusy(true); setError(""); setMessage("");
    try {
      const row = await api("/owner/api/review-policy", {method:"POST", body:JSON.stringify({csrf, expected_version:record.version, settings:nextSettings, api_key:useProviderInput ? apiKey || undefined : undefined, delete_key:useProviderInput && removeKey})});
      setRecord(row); setSettings({...row.settings, criteria:settings.criteria}); setApiKey(""); setRemoveKey(false);
      setMessage("Settings saved."); onSaved();
    } catch (e:any) { setError(e.message); }
    finally { setBusy(false); }
  }
  async function save(e:React.FormEvent) {
    e.preventDefault();
    await activate(settingsForOwnerSave({...settings, criteria:record.settings.criteria}));
  }
  async function saveCriteria(e:React.FormEvent) {
    e.preventDefault();
    setBusy(true); setCriteriaError(""); setCriteriaMessage("");
    try {
      const row = await api("/owner/api/review-criteria", {method:"POST", body:JSON.stringify({csrf, expected_version:record.version, criteria:settings.criteria})});
      setRecord(row);
      // Retain unsaved model settings; this action saves only the criteria text.
      setSettings((current:any)=>({...current, criteria:row.settings.criteria}));
      setCriteriaMessage("Review criteria saved."); onSaved();
    } catch (e:any) { setCriteriaError(e.message); }
    finally { setBusy(false); }
  }
  const criteriaPrompt = `Help me write criteria for reviewing findings in Proofpress.

Use what you know about my workflow. Ask up to three short questions if needed.
Describe:
- What evidence a finding needs
- When evidence is insufficient or contradictory
- When to flag uncertainty for human review

Return readable text or bullets, without JSON or a code block.
I will review and save it. Do not include secrets or change approval permissions.`;
  async function copyPrompt() {
    try { await navigator.clipboard.writeText(criteriaPrompt); setCopied(true); setShowAuthoringPrompt(false); }
    catch { setCopied(false); setShowAuthoringPrompt(true); }
  }
  const criteriaChanged = record && settings && (record.version === 0 || settings.criteria !== record.settings.criteria);
  const changed = record && settings && (settings.mode !== "off" || record.settings.mode !== "off") &&
    (JSON.stringify({...settings, criteria:""}) !== JSON.stringify({...record.settings, criteria:""}) || !!apiKey || removeKey);
  const hasProviderCredential = providerCredentialReady(record, settings, apiKey, removeKey);
  const selectedProvider = record?.providers?.[settings?.provider];
  const savedByok = Boolean(record?.settings?.provider === settings?.provider && record?.credential?.configured && !record?.credential?.managed);
  const modelOptions = providerModelOptions(selectedProvider, settings?.model || "");
  const missingProviderKey = settings?.mode !== "off" && !hasProviderCredential;
  return <>
    <Card className="reviewPolicy reviewCriteria">
      <CardHeader className="policyHeading"><div><h2 id="reviewCriteriaTitle">Review criteria</h2><CardDescription>Define the evidence and limits you check before approving a finding. Save these independently of AI-assisted checks.</CardDescription></div></CardHeader>
      <CardContent>
        {record && <PolicyHistory api={api} kind="criteria" currentVersion={record.version} currentContent={record.settings.criteria} contentOf={row=>row.criteria || ""} />}
        {!settings ? <p role="status">Loading review criteria…</p> : <form onSubmit={saveCriteria}>
          <fieldset disabled={busy}>
      <div className="simpleCriteria">
        <div className="simplePromptRow capturePromptRow"><h3>Draft review criteria with your agent</h3><pre className="agentPrompt" aria-label="Policy authoring prompt"><code>{criteriaPrompt}</code></pre><Button type="button" onClick={copyPrompt}>{copied ? <><Check />Copied</> : "Copy prompt"}</Button></div>
        <div className="simpleCopyStatus" role="status" aria-live="polite">{copied ? "Copied — paste into your agent’s chat." : showAuthoringPrompt ? "Copy failed. Select and copy the prompt above." : ""}</div>
        <p className="draftPasteHelp">Paste your agent’s draft below, then review and save.</p>
        <MarkdownEditor label="Review criteria" value={settings.criteria} maxLength={8000} placeholder="Paste your agent's criteria, or write your own." onChange={value=>{change("criteria",value);setCriteriaMessage("");}} />
      </div>
          </fieldset>
          <p className="policyHint">Saving criteria does not enable AI, change approval settings or start a model review.</p>
          <div className="policyFooter"><small>{record.version ? `Saved version ${record.version}${criteriaChanged ? " · Unsaved criteria" : ""}` : "Human review is available without a model."}</small><Button disabled={busy || !criteriaChanged || !csrf}>{busy ? "Saving…" : "Save review criteria"}</Button></div>
        </form>}
        {criteriaError && <div className="policyError" role="alert">{criteriaError} <Button variant="outline" onClick={load}>Reload settings</Button></div>}
        {criteriaMessage && <p className="copySuccess" role="status">{criteriaMessage}</p>}
      </CardContent>
    </Card>
    <Card id="review-policy-setup" className={`reviewPolicy verificationSettings${settings?.mode === "off" && !changed && !message && !error ? " aiChecksCompact" : ""}`} aria-labelledby="reviewPolicyTitle">
    <CardHeader className="policyHeading aiChecksHeading"><div><h2 id="reviewPolicyTitle">AI-assisted checks</h2><CardDescription id="llm-checks-help">{!settings ? "Choose whether AI helps review findings." : settings.mode === "off" ? "You review findings yourself. Turn this on to get an AI assessment before you decide." : settings.auto_admit_new_claims ? "AI checks new findings after evidence checks pass. Your approval rules below determine which findings can be reused." : "AI checks new findings after evidence checks pass. You still decide what agents can reuse."}</CardDescription></div>
      {settings && <div className="aiChecksControl"><span>{settings.mode === "off" ? "Off" : "On"}</span><Switch aria-labelledby="reviewPolicyTitle" aria-describedby="llm-checks-help" checked={settings.mode !== "off"} disabled={busy} onCheckedChange={enabled=>{setSettings({...settings,mode:enabled ? "automatic" : "off",require_judge:enabled ? settings.require_judge : false,auto_admit_new_claims:enabled ? settings.auto_admit_new_claims : false});setMessage("");}} /></div>}
    </CardHeader>
    {error && <div className="policyError" role="alert">{error} <Button variant="outline" onClick={load}>Reload settings</Button></div>}
    {!settings ? <CardContent><p role="status">Loading verification settings…</p></CardContent> : <CardContent>
      <form onSubmit={save}>
        {settings.mode !== "off" && <div className="modelAdviceConfiguration">
<Disclosure className="modelConnection" defaultOpen={!record.credential.configured}><DisclosureTrigger>Model connection</DisclosureTrigger><DisclosureContent>
<fieldset aria-label="Model connection">
        <div className="policyFields three">
          <Label>Provider<NativeSelect aria-label="Model provider" value={settings.provider} onChange={e=>{setSettings(applyProviderPreset(settings,e.target.value,record.providers));setApiKey("");setRemoveKey(false);setMessage("");}}>{Object.entries(record.providers).map(([key,value]:any)=><option key={key} value={key}>{key === "typesafe" ? "TypeSafe" : key === "vercel_jev" ? "Vercel AI Gateway · Jev" : value.label}</option>)}</NativeSelect></Label>
          <Label>Model{modelOptions.length>0 && <NativeSelect aria-label="Model" value={selectedProvider.models.includes(settings.model)?settings.model:"__custom__"} onChange={e=>change("model",e.target.value==="__custom__"?"":e.target.value)}>
            {modelOptions.filter((model:string)=>selectedProvider.models.includes(model)).map((model:string)=><option key={model} value={model}>{model}</option>)}
            {!["managed_gmi", "openai_decisions"].includes(settings.provider) && <option value="__custom__">Enter another model ID…</option>}
          </NativeSelect>}
            {(modelOptions.length===0 || !selectedProvider.models.includes(settings.model)) && <Input aria-label="Custom model ID" value={settings.model} placeholder={selectedProvider?.editable_model?"deployment-or-model-name":"provider/model-name"} onChange={e=>change("model",e.target.value)} />}
            <small>{settings.provider === "managed_gmi" ? "GPT-6 Luna via GMI Cloud. LLM advice; human approval required." : settings.provider === "openai_decisions" ? "Uses the dedicated OpenAI Decisions API." : "Choose a provider model or enter another supported model ID."}</small></Label>

          {(selectedProvider?.endpoint_required || selectedProvider?.endpoint_editable) && <Label className="wide">HTTPS endpoint<Input type="url" required={settings.mode!=="off" && selectedProvider.endpoint_required} value={settings.endpoint} placeholder={selectedProvider.endpoint_placeholder} onChange={e=>change("endpoint",e.target.value)} />{selectedProvider.endpoint_editable && <small>Leave blank to use the provider's hosted endpoint.</small>}</Label>}
        </div>
        {selectedProvider?.managed ? <p className="policyHint">{selectedProvider.available ? "Hosted verification uses an operator-managed key. No API key needed. Choose another provider to use your own key." : "Hosted verification is awaiting operator setup. You can keep human review or choose a provider with your own key."}</p> : <div className="providerCredential"><Label>API key<Input type="password" autoComplete="new-password" value={apiKey} disabled={removeKey || !record.credential.storage_ready} placeholder={!record.credential.storage_ready ? "Key storage is not configured" : savedByok ? `Saved key ending in ${record.credential.last_four || "••••"}` : "Paste a provider key"} onChange={e=>setApiKey(e.target.value)} /></Label>
          <p>{!record.credential.storage_ready ? "Provider API keys cannot be saved until encrypted storage is configured." : savedByok ? "A write-only credential is stored for this workspace." : "The key is encrypted for this workspace and never returned to the browser."}</p>
          {savedByok && <Label className="policyCheck"><Checkbox checked={removeKey} onCheckedChange={checked=>{setRemoveKey(checked === true);setApiKey("");}} />Remove stored key when saving</Label>}
          {!record.credential.storage_ready && <p className={localPreview ? "policyHint" : "policyWarning"} role="note">{localPreview ? "This local preview has no encrypted key storage. Human review and agent connections are available." : "Ask your hosting operator to configure encrypted credential storage before adding a provider key. Human review and agent connections are available."}</p>}
        </div>}
      </fieldset>
      </DisclosureContent></Disclosure>
      <Disclosure className="providerPrivacy"><DisclosureTrigger>Advanced settings</DisclosureTrigger><DisclosureContent>
        {["openrouter", "vercel_jev"].includes(settings.provider) ? <Label className="policyCheck"><Checkbox checked={settings.zdr} onCheckedChange={checked=>change("zdr",checked === true)} />Require {settings.provider === "vercel_jev" ? "Vercel Gateway" : "OpenRouter"} Zero Data Retention routing</Label> : <p>Proofpress cannot enforce Zero Data Retention routing for this provider. Its data retention terms apply.</p>}
      </DisclosureContent></Disclosure>

        </div>}
        {settings.mode !== "off" && !(settings.require_judge || settings.auto_admit_new_claims || record.settings.require_judge || record.settings.auto_admit_new_claims) && <p className="policyHint">AI provides an assessment. You make the final approval.</p>}
        {settings.mode !== "off" && Boolean(settings.require_judge || settings.auto_admit_new_claims || record.settings.require_judge || record.settings.auto_admit_new_claims) && <Disclosure className="verificationAutomatic" defaultOpen={Boolean(settings.require_judge || settings.auto_admit_new_claims)}><DisclosureTrigger>Approval options</DisclosureTrigger><DisclosureContent>
        <Label className="policyCheck"><Checkbox checked={settings.require_judge} onCheckedChange={checked=>setSettings({...settings,require_judge:checked === true,auto_admit_new_claims:checked === true ? settings.auto_admit_new_claims : false})} />Require supporting model advice before human approval</Label>
<fieldset className="autoAdmissionFieldset">
        <Label className="policyCheck autoAdmissionToggle"><Checkbox checked={settings.auto_admit_new_claims === true} disabled={!settings.auto_admit_new_claims && (settings.mode !== "automatic" || !settings.require_judge || !record.settings.criteria.trim() || !hasProviderCredential)} onCheckedChange={checked=>change("auto_admit_new_claims",checked === true)} /><span><b>Approve qualifying new claims automatically</b><small>Applies to qualifying new claims, including high-risk claims. Requested revisions still need human approval.</small></span></Label>
        {settings.auto_admit_new_claims ? <div className="policyWarning autoAdmissionWarning" role="note"><strong>Automatic approval will take effect when you save.</strong><p>Scope: new claims in this workspace, including high-risk claims, except requested revisions. Requested revisions always need human approval. New claims enter approved knowledge when current checks pass, there is no unresolved conflict or invalid dependency, and the configured model recommends “Evidence supported.” Claims the model rejects, escalates, or cannot review stay for your decision. Qualifying claims will not receive per-claim human approval. Model recommendations are not calibrated probabilities.</p></div> : <p className="policyHint">Off by default. Requires supporting model advice, review criteria, a valid API key, and permission to process evidence.</p>}
      </fieldset>
        </DisclosureContent></Disclosure>}
        {(changed || busy) && settings.mode !== "off" && <p className="providerConsentNotice" role="note">Findings and their supporting evidence will be sent to <strong>{selectedProvider?.label || settings.provider}</strong>{settings.endpoint ? <> at <strong>{settings.endpoint}</strong></> : null} for AI review. By saving AI settings, you authorize this processing for this workspace. Automatic review also checks existing pending findings and may incur provider usage charges. Approval remains separate.</p>}
        {(changed || busy) && <div className="policyFooter"><small>{record.version ? "Unsaved changes" : "Evidence checks are included in either option."}</small><Button disabled={busy || !changed || !csrf || missingProviderKey}>{busy ? "Saving…" : settings.auto_admit_new_claims ? "Save & enable automatic approval" : settings.mode !== "off" && (record.settings.mode === "off" || !record.settings.external_consent || record.settings.provider !== settings.provider || record.settings.endpoint !== settings.endpoint) ? "Enable AI checks" : "Save AI settings"}</Button></div>}
        {missingProviderKey && <p role="note" className="policyHint">{selectedProvider?.managed ? "Hosted verification is not ready. Human review remains available." : "Add a provider API key to enable AI checks, or turn them off to use manual review."}</p>}
      </form>
      {message && <p className="copySuccess" role="status"><HugeiconsIcon icon={CheckmarkCircle02Icon}/>{message}</p>}
    </CardContent>}
  </Card></>;
}
