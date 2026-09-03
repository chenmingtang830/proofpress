import React from "react";
import { Button } from "./ui/button";

export function ReviewPolicy({csrf, api, onSaved}: any) {
  const [record, setRecord] = React.useState<any>(null);
  const [settings, setSettings] = React.useState<any>(null);
  const [busy, setBusy] = React.useState(false);
  const [message, setMessage] = React.useState("");
  const [error, setError] = React.useState("");
  const load = React.useCallback(async () => {
    try { const row = await api("/owner/api/review-policy"); setRecord(row); setSettings(row.settings); setError(""); }
    catch (e:any) { setError(e.message); }
  }, [api]);
  React.useEffect(() => { void load(); }, [load]);
  const change = (key:string, value:any) => { setSettings({...settings, [key]:value}); setMessage(""); };
  async function save(e:React.FormEvent) {
    e.preventDefault(); setBusy(true); setError(""); setMessage("");
    try {
      const row = await api("/owner/api/review-policy", {method:"POST", body:JSON.stringify({csrf, expected_version:record.version, settings})});
      setRecord(row); setSettings(row.settings); setMessage(`Review policy saved · version ${row.version}`); onSaved();
    } catch (e:any) { setError(e.message); }
    finally { setBusy(false); }
  }
  return <section className="reviewPolicy" aria-labelledby="reviewPolicyTitle">
    <h2 id="reviewPolicyTitle">Review policy</h2>
    <p>Choose when evidence receives LM advice. You still make the final decision.</p>
    {error && <div role="alert">{error} <Button variant="outline" onClick={load}>Reload settings</Button></div>}
    {!settings ? <p role="status">Loading review policy…</p> : <form onSubmit={save}>
      <h3>Provider</h3>
      <div className="policyFields">
        <label htmlFor="lm-review-mode">LM review<select id="lm-review-mode" aria-label="LM review" value={settings.mode} onChange={e=>change("mode",e.target.value)}><option value="off">Off</option><option value="manual">Run when requested</option><option value="automatic">Automatically after checks pass</option></select></label>
        <label>OpenRouter model<input value={settings.model} placeholder="deepseek/deepseek-v4-flash" onChange={e=>change("model",e.target.value)} /></label>
        <label>Evaluation criteria<select value={settings.rubric} onChange={e=>change("rubric",e.target.value)}>{Object.entries(record.rubrics).map(([key,label]:any)=><option key={key} value={key}>{label} · {key}</option>)}</select></label>
      </div>
      {!record.provider_ready && <p>Server API key is not configured. Add OPENROUTER_API_KEY in Render before enabling LM review.</p>}
      <h3>Data sharing</h3>
      <p>When LM review runs, the conclusion and its bounded evidence text leave this workspace for OpenRouter and the selected model provider. The API key remains server-side.</p>
      <label className="policyCheck"><input type="checkbox" checked={settings.external_consent} onChange={e=>change("external_consent",e.target.checked)} />Allow this workspace to send conclusions and bound evidence to OpenRouter for review</label>
      <h3>Approval requirement</h3>
      <label className="policyCheck"><input type="checkbox" checked={settings.require_judge} onChange={e=>change("require_judge",e.target.checked)} />Require current, supporting LM advice before approval</label>
      <p>{settings.require_judge ? "Approval stays unavailable after provider failure until supporting advice is recorded." : "You may still approve after deterministic checks pass when advice is missing or unavailable."}</p>
      <p className="policyCaution">Changing criteria, model or approval requirements can make existing advice and admissions stale. “Current” means the advice matches this policy version and conclusion. Automatic review applies to new proposals only; it does not process your backlog.</p>
      <div className="policyFooter"><small>{record.version ? `Policy version ${record.version} · last changed by ${record.actor}` : "Using deployment defaults · save to create this workspace’s first policy"}</small><Button disabled={busy || JSON.stringify(settings)===JSON.stringify(record.settings)}>{busy?"Saving…":"Save review policy"}</Button></div>
      {message && <p className="copySuccess" role="status">{message}</p>}
    </form>}
  </section>;
}
