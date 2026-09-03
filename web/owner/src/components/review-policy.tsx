import React from "react";
import { CheckmarkCircle02Icon, Copy01Icon } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { Button } from "./ui/button";

export function ReviewPolicy({csrf, api, onSaved}: any) {
  const [record, setRecord] = React.useState<any>(null);
  const [settings, setSettings] = React.useState<any>(null);
  const [apiKey, setApiKey] = React.useState("");
  const [removeKey, setRemoveKey] = React.useState(false);
  const [busy, setBusy] = React.useState(false);
  const [message, setMessage] = React.useState("");
  const [error, setError] = React.useState("");
  const [draft, setDraft] = React.useState("");
  const [copied, setCopied] = React.useState(false);
  const load = React.useCallback(async () => {
    try {
      const row = await api("/owner/api/review-policy");
      setRecord(row);
      setSettings(row.version === 0 ? {...row.settings, mode:"automatic", require_judge:true} : row.settings);
      setError("");
    }
    catch (e:any) { setError(e.message); }
  }, [api]);
  React.useEffect(() => { void load(); }, [load]);
  const change = (key:string, value:any) => { setSettings({...settings, [key]:value}); setMessage(""); };
  async function save(e:React.FormEvent) {
    e.preventDefault(); setBusy(true); setError(""); setMessage("");
    try {
      const row = await api("/owner/api/review-policy", {method:"POST", body:JSON.stringify({csrf, expected_version:record.version, settings, api_key:apiKey || undefined, delete_key:removeKey})});
      setRecord(row); setSettings(row.settings); setApiKey(""); setRemoveKey(false);
      setMessage(`Policy v${row.version} is active`); onSaved();
    } catch (e:any) { setError(e.message); }
    finally { setBusy(false); }
  }
  async function copyPrompt() {
    try { await navigator.clipboard.writeText(record.authoring_prompt); setCopied(true); }
    catch { setError("Your browser blocked copying. Select the prompt and copy it manually."); }
  }
  function applyDraft() {
    try {
      const parsed = JSON.parse(draft);
      const allowed = ["provider","endpoint","model","criteria","zdr","mode","require_judge","external_consent"];
      if (!parsed || typeof parsed !== "object" || allowed.some(key => !(key in parsed))) throw new Error();
      setSettings(Object.fromEntries(allowed.map(key => [key, parsed[key]])));
      setDraft(""); setError(""); setMessage("Agent-authored policy loaded for review. Save to activate it.");
    } catch { setError("Paste the complete JSON policy returned by your agent."); }
  }
  const changed = record && settings && (JSON.stringify(settings)!==JSON.stringify(record.settings) || !!apiKey || removeKey);
  return <section className="reviewPolicy" aria-labelledby="reviewPolicyTitle">
    <div className="policyHeading"><div><h2 id="reviewPolicyTitle">Judge & policy</h2><p>Configure advisory review for this workspace. Human approval remains required.</p></div>{record?.version > 0 && <span>Policy v{record.version}</span>}</div>
    {error && <div className="policyError" role="alert">{error} <Button variant="outline" onClick={load}>Reload</Button></div>}
    {!settings ? <p role="status">Loading policy…</p> : <form onSubmit={save}>
      <fieldset><legend>Model provider</legend>
        <div className="policyFields three">
          <label>Provider<select aria-label="Model provider" value={settings.provider} onChange={e=>change("provider",e.target.value)}>{Object.entries(record.providers).map(([key,value]:any)=><option key={key} value={key}>{value.label}</option>)}</select></label>
          <label>Model<input value={settings.model} placeholder={settings.provider==="anthropic"?"claude-sonnet-4-5":"provider/model-name"} onChange={e=>change("model",e.target.value)} /></label>
          <label>LM review<select aria-label="LM review" value={settings.mode} onChange={e=>{const mode=e.target.value;setSettings({...settings,mode,require_judge:mode==="off"?false:settings.require_judge});setMessage("");}}><option value="off">Off</option><option value="manual">Run when requested</option><option value="automatic">After checks pass</option></select></label>
          {settings.provider==="custom" && <label className="wide">HTTPS endpoint<input type="url" value={settings.endpoint} placeholder="https://models.example.com/v1/chat/completions" onChange={e=>change("endpoint",e.target.value)} /></label>}
        </div>
        <div className="providerCredential"><label>API key<input type="password" autoComplete="new-password" value={apiKey} disabled={removeKey} placeholder={record.credential.configured ? `Saved key ending in ${record.credential.last_four || "••••"}` : "Paste a provider key"} onChange={e=>setApiKey(e.target.value)} /></label>
          <p>{record.credential.configured ? "A write-only credential is stored for this workspace." : "The key is encrypted for this workspace and never returned to the browser."}</p>
          {record.credential.configured && <label className="policyCheck"><input type="checkbox" checked={removeKey} onChange={e=>{setRemoveKey(e.target.checked);setApiKey("");}} />Remove stored key when saving</label>}
          {!record.credential.storage_ready && <p className="policyWarning">Secure credential storage is unavailable on this deployment.</p>}
        </div>
      </fieldset>
      <fieldset><legend>Evaluation</legend>
        <label className="criteriaLabel">Criteria<textarea value={settings.criteria} maxLength={8000} placeholder="What evidence must support a conclusion? When should the judge escalate?" onChange={e=>change("criteria",e.target.value)} /></label>
        <details className="agentPolicyDraft"><summary>Draft criteria with your agent</summary><p>Copy a safe authoring prompt to your own agent. It will interview you and return a policy you can review here. Never include an API key.</p>
          <div className="policyPrompt"><textarea readOnly value={record.authoring_prompt} aria-label="Policy authoring prompt" /><Button type="button" variant="outline" onClick={copyPrompt}>{copied?<><HugeiconsIcon icon={CheckmarkCircle02Icon}/>Copied</>:<><HugeiconsIcon icon={Copy01Icon}/>Copy prompt</>}</Button></div>
          <label className="criteriaLabel">Agent response<textarea value={draft} placeholder="Paste the JSON policy from your agent" onChange={e=>setDraft(e.target.value)} /></label><Button type="button" variant="outline" disabled={!draft.trim()} onClick={applyDraft}>Load for review</Button>
        </details>
      </fieldset>
      <fieldset><legend>Data & approval</legend>
        <p>LM review sends the conclusion and bounded evidence to the selected provider. The recommendation is advisory.</p>
        <label className="policyCheck"><input type="checkbox" checked={settings.external_consent} onChange={e=>change("external_consent",e.target.checked)} />Allow external model processing for this workspace</label>
        {settings.provider==="openrouter" && <label className="policyCheck"><input type="checkbox" checked={settings.zdr} onChange={e=>change("zdr",e.target.checked)} />Require OpenRouter Zero Data Retention routing</label>}
        <label className="policyCheck"><input type="checkbox" checked={settings.require_judge} onChange={e=>change("require_judge",e.target.checked)} />Require current supporting LM advice before human approval</label>
      </fieldset>
      <div className="policyFooter"><small>{record.version ? `Changed by ${record.actor} · ${record.policy_digest.slice(0,18)}…` : "Using deployment defaults"}</small><Button disabled={busy || !changed}>{busy?"Saving…":"Save & activate"}</Button></div>
      {message && <p className="copySuccess" role="status"><HugeiconsIcon icon={CheckmarkCircle02Icon}/>{message}</p>}
    </form>}
  </section>;
}
