import React from "react";
import { Card, CardHeader, CardDescription, CardContent } from "./ui/card";
import { MarkdownEditor } from "./ui/markdown-editor";
import { Button } from "./ui/button";
import { Check } from "./ui/icon";
import { PolicyHistory } from "./policy-history";

export const RESEARCH_OVER_TIME_RULES = {
  purpose: "Accumulate evidence-backed observations, changing views and later outcomes across recurring research. Use the past 30 days to inform the next brief; keep older history for audit.",
  capture: [
    "One verifiable observation, change or outcome per finding. Add stable topic tags, the instrument or population, effective date, report date and known availability time.",
    "Compare a new report with earlier findings on the same topic. Submit a material change or independent corroboration with references to both sources; preserve differences in sample, units and horizon.",
    "Attach bounded evidence with the source filename and section, or sheet, date, instrument, field and cell. Keep reported facts separate from the agent's interpretation.",
    "When later data answers an earlier question, link to the original finding and its recorded horizon, target and conditions. Label the outcome supported, contradicted or still unresolved, with evidence.",
    "Extract a reusable lesson only from comparable cases, with counterevidence and limits. Distinguish historical reconstruction from information demonstrably available at the time.",
    "Before writing, retrieve relevant, eligible findings from the past 30 days using the writing cutoff. Keep approved context, staged drafts and open watches separate. The time window is not a deletion rule."
  ],
  exclude: [
    "Repeated report text or the same chart counted as independent corroboration; unchanged daily snapshots with no research question.",
    "Predictions, targets or evaluation deadlines invented after observing outcomes; unknown timestamps treated as known.",
    "Price moves presented as proof of flows, causality or a different basket's performance; missing observations treated as zero.",
    "Raw source dumps, credentials, routine progress updates or unvalidated hypotheses presented as established findings."
  ]
};

export function captureDraftPrompt(_record: any) {
  return `Help me decide what my agent should submit to Proofpress.

Use what you know about my workflow. Ask up to three focused questions if needed.
Draft short rules with these headings:
## Purpose
## Capture
## Leave out
Explain the purpose in one short paragraph. List information to submit under Capture and information to skip under Leave out, as bullets.

Return readable text, without JSON or a code block. I will review and save it.
Keep the purpose under 1,000 characters and each list to 30 rules of at most 500 characters. Include at least one capture rule.
Do not include secrets or change approval permissions.`;
}

export function parseCaptureDraft(text: string) {
  const clean = text.trim().replace(/^\x60\x60\x60(?:json)?\s*([\s\S]*?)\s*\x60\x60\x60$/i, "$1");
  const value = JSON.parse(clean);
  if (!value || typeof value !== "object" || Array.isArray(value) ||
      Object.keys(value).sort().join(",") !== "capture,exclude,purpose") throw new Error("Use only purpose, capture and exclude fields.");
  if (typeof value.purpose !== "string" || !value.purpose.trim() || value.purpose.length > 1000) throw new Error("Purpose must be 1–1,000 characters.");
  for (const key of ["capture", "exclude"]) {
    if (!Array.isArray(value[key]) || value[key].length > 30 || (key === "capture" && !value[key].length) ||
        value[key].some((item: any) => typeof item !== "string" || !item.trim() || item.length > 500)) throw new Error("Use up to 30 rules in each list, with at least one capture rule. Each rule must be 1–500 characters.");
  }
  return {purpose:value.purpose.trim(),capture:value.capture.map((line:string)=>line.trim()),exclude:value.exclude.map((line:string)=>line.trim())};
}

export function formatCaptureRules(settings: {purpose:string; capture:string[]; exclude:string[]}) {
  const bullets = (items:string[]) => items.map(item=>`- ${item.replace(/\n/g, "\n  ")}`).join("\n");
  return `## Purpose\n${settings.purpose}\n\n## Capture\n${bullets(settings.capture)}\n\n## Leave out\n${bullets(settings.exclude)}`;
}

export function parseCaptureText(text:string) {
  if (/^\s*(?:\{|`{3}json)/.test(text)) return parseCaptureDraft(text);
  const sections:Record<string,string[]> = {};
  let current = "";
  for (const line of text.split(/\r?\n/)) {
    const heading = line.match(/^##\s+(Purpose|Capture|Leave out)\s*$/i);
    if (heading) {
      current = heading[1].toLowerCase();
      if (sections[current]) throw new Error("Use each heading once: ## Purpose, ## Capture, ## Leave out.");
      sections[current] = [];
    } else if (current) sections[current].push(line);
    else if (line.trim()) throw new Error("Keep the three headings: ## Purpose, ## Capture, ## Leave out.");
  }
  if (Object.keys(sections).length !== 3) throw new Error("Keep the three headings: ## Purpose, ## Capture, ## Leave out.");
  const items = (lines:string[]) => {
    const result:string[] = [];
    for (const line of lines) {
      if (!line.trim()) continue;
      const bullet = line.match(/^[-*+]\s+(.*)$/);
      if (bullet) result.push(bullet[1]);
      else if (/^\s+/.test(line) && result.length) result[result.length-1] += "\n" + line.trim();
      else throw new Error("Write each capture or exclusion rule as a bullet starting with -.");
    }
    return result;
  };
  return parseCaptureDraft(JSON.stringify({purpose:sections.purpose.join("\n").trim(),capture:items(sections.capture),exclude:items(sections["leave out"])}));
}

export function CaptureRules({api, csrf}: any) {
  const [record, setRecord] = React.useState<any>(null);
  const [text, setText] = React.useState("");
  const [error, setError] = React.useState("");
  const [message, setMessage] = React.useState("");
  const [busy, setBusy] = React.useState(false);
  const [copyStatus, setCopyStatus] = React.useState("");
  const load = React.useCallback(async () => {
    try {
      const row = await api("/owner/api/capture-policy");
      setRecord(row); setText(formatCaptureRules(row.settings)); setError("");
    } catch (e:any) { setError(e.message); }
  }, [api]);
  React.useEffect(()=>{void load();},[load]);
  const changed = record && text !== formatCaptureRules(record.settings);
  async function copyPrompt() {
    try { await navigator.clipboard.writeText(captureDraftPrompt(record)); setCopyStatus("copied"); }
    catch { setCopyStatus("failed"); }
  }
  async function save(event:React.FormEvent) {
    event.preventDefault(); setError(""); setMessage("");
    let settings;
    try { settings = parseCaptureText(text); }
    catch (e:any) { setError(e.message); return; }
    setBusy(true);
    try {
      const row = await api("/owner/api/capture-policy", {method:"POST",body:JSON.stringify({csrf,expected_version:record.version,settings})});
      setRecord(row); setText(formatCaptureRules(row.settings)); setCopyStatus("");
      setMessage(`Capture rules v${row.version} saved. Agents will use them on their next run.`);
    } catch (e:any) { setError(e.message); }
    finally { setBusy(false); }
  }
  return <Card className="captureRules captureRulesSimple">
    <CardHeader className="adminPanelHeading"><h2>What should the agent capture?</h2><CardDescription>Tell the agent which information to submit to Proofpress for review and which to skip. Your agent runs these rules; saving them does not schedule research or scan old reports.</CardDescription></CardHeader>
    <CardContent>
      {record && <PolicyHistory api={api} kind="capture" currentVersion={record.version} currentContent={formatCaptureRules(record.settings)} contentOf={row=>formatCaptureRules(row.settings)} />}
      {error && <p role="alert">{error} {!record && <Button variant="outline" onClick={load}>Try again</Button>}</p>}
      {!record ? <p role="status">Loading rules…</p> : <form onSubmit={save}>
        <div className="simplePromptRow"><p>Build on recurring topics, track changes and check later outcomes.</p><Button type="button" variant="outline" onClick={()=>{setText(formatCaptureRules(RESEARCH_OVER_TIME_RULES));setMessage("Research template loaded. Adjust the topics and review before saving.");setError("");}}>Load research over time template</Button></div>
        <div className="simplePromptRow capturePromptRow"><h3>Draft capture rules with your agent</h3><pre className="agentPrompt" aria-label="Capture rules authoring prompt"><code>{captureDraftPrompt(record)}</code></pre><Button type="button" onClick={copyPrompt}>{copyStatus === "copied" ? <><Check />Copied</> : "Copy prompt"}</Button></div>
        <div className="simpleCopyStatus" role="status" aria-live="polite">{copyStatus === "copied" ? "Copied — paste into your agent’s chat." : copyStatus === "failed" ? "Copy failed. Select and copy the prompt above." : ""}</div>
        <p className="draftPasteHelp">Paste your agent’s draft below, then review and save.</p>
        <MarkdownEditor className="captureRulesEditor" label="Capture rules" value={text} maxLength={40000} onChange={value=>{setText(value);setMessage("");setError("");}} />
        <div className="policyFooter"><small>{changed ? "Unsaved changes" : record.version ? `Saved · version ${record.version}` : "Defaults are ready to use"}</small><Button disabled={busy || !changed || !csrf}>{busy ? "Saving…" : "Save capture rules"}</Button></div>
      </form>}
      {message && <p role="status">{message}</p>}
    </CardContent>
  </Card>;
}
