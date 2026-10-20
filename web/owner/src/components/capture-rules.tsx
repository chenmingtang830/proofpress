import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./ui/card";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Button } from "./ui/button";

export function CaptureRules({api, csrf}: any) {
  const [record, setRecord] = React.useState<any>(null);
  const [purpose, setPurpose] = React.useState("");
  const [capture, setCapture] = React.useState("");
  const [exclude, setExclude] = React.useState("");
  const [error, setError] = React.useState("");
  const [message, setMessage] = React.useState("");
  const [busy, setBusy] = React.useState(false);
  const load = React.useCallback(async () => {
    try {
      const row = await api("/owner/api/capture-policy");
      setRecord(row); setPurpose(row.settings.purpose);
      setCapture(row.settings.capture.join("\n")); setExclude(row.settings.exclude.join("\n")); setError("");
    } catch (e: any) { setError(e.message); }
  }, [api]);
  React.useEffect(() => { void load(); }, [load]);
  const rules = (value: string) => value.split("\n").map(line => line.trim()).filter(Boolean);
  const settings = {purpose, capture:rules(capture), exclude:rules(exclude)};
  const changed = record && JSON.stringify(settings) !== JSON.stringify(record.settings);
  async function save(event: React.FormEvent) {
    event.preventDefault(); setBusy(true); setError(""); setMessage("");
    try {
      const row = await api("/owner/api/capture-policy", {method:"POST", body:JSON.stringify({csrf,expected_version:record.version,settings})});
      setRecord(row); setPurpose(row.settings.purpose); setCapture(row.settings.capture.join("\n")); setExclude(row.settings.exclude.join("\n"));
      setMessage(`Capture rules v${row.version} saved. Connected agents read them at the start of their next run.`);
    } catch (e: any) { setError(e.message); }
    finally { setBusy(false); }
  }
  return <Card className="captureRules"><CardHeader><CardTitle>What agents should capture</CardTitle>
    <CardDescription>Workspace defaults work immediately. Customize them here; no local policy file is required.</CardDescription></CardHeader>
    <CardContent>
      {error && <p role="alert">{error} <Button variant="outline" onClick={load}>Reload capture rules</Button></p>}
      {!record ? <p role="status">Loading capture rules…</p> : <form onSubmit={save}>
        <Label>Research purpose<Textarea aria-label="Research purpose" value={purpose} maxLength={1000} onChange={e=>setPurpose(e.target.value)} required /></Label>
        <Label>Capture these findings<Textarea aria-label="Capture these findings" value={capture} onChange={e=>setCapture(e.target.value)} required /><small>One rule per line. Up to 30 rules.</small></Label>
        <Label>Leave these out<Textarea aria-label="Leave these out" value={exclude} onChange={e=>setExclude(e.target.value)} /><small>One exclusion per line. Local project restrictions may further narrow these rules.</small></Label>
        <p>Capture rules guide what agents propose. Evidence checks and owner approval still control reuse. Secrets and raw private traces remain excluded.</p>
        <div className="policyFooter"><small>{record.version ? `Version ${record.version} · ${record.actor}` : "Built-in defaults active"}</small><Button disabled={busy || !changed || !csrf}>{busy ? "Saving…" : "Save capture rules"}</Button></div>
      </form>}
      {message && <p role="status">{message}</p>}
    </CardContent></Card>;
}
