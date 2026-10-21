import React from "react";
import { Button } from "./ui/button";
import { NativeSelect } from "./ui/native-select";
import { Label } from "./ui/label";
import { Disclosure, DisclosureTrigger, DisclosureContent } from "./ui/disclosure";
import "./policy-history.css";

type Version = {version:number; actor:string|null; updated_at:string|null; criteria?:string; settings?:any};
type History = {versions:Version[]; current_version:number; next_before_version:number|null};
const savedTime = (value:string|null) => {
  if (!value) return "Time not recorded";
  const date = new Date(value);
  return Number.isNaN(date.valueOf()) ? value : date.toLocaleString();
};

/** Browsing immutable saved text never changes the editor or activates a policy. */
export function PolicyHistory({api, kind, currentVersion, currentContent, contentOf}: {
  api:(path:string)=>Promise<History>; kind:"capture"|"criteria"; currentVersion:number; currentContent:string;
  contentOf:(row:Version)=>string;
}) {
  const title = kind === "capture" ? "Capture rules" : "Review criteria";
  const endpoint = kind === "capture" ? "/owner/api/capture-policy/history" : "/owner/api/review-criteria/history";
  const [open, setOpen] = React.useState(false);
  const [rows, setRows] = React.useState<Version[]>([]);
  const [selected, setSelected] = React.useState<number|null>(null);
  const [next, setNext] = React.useState<number|null>(null);
  const [latest, setLatest] = React.useState(currentVersion);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [reload, setReload] = React.useState(0);
  const [compare, setCompare] = React.useState(false);
  const epoch = React.useRef(0);
  React.useEffect(()=>{
    const request = ++epoch.current;
    if (!open) return;
    setLoading(true); setError(""); setRows([]); setNext(null); setSelected(null);
    void api(endpoint).then(result=>{
      if (request !== epoch.current) return;
      setRows(result.versions); setNext(result.next_before_version); setLatest(result.current_version);
      setSelected((result.versions.find(row=>row.version < currentVersion) || result.versions[0])?.version ?? null);
    }).catch((e:Error)=>{if (request === epoch.current) setError(e.message);})
      .finally(()=>{if (request === epoch.current) setLoading(false);});
    return ()=>{++epoch.current;};
  },[api,endpoint,open,currentVersion,reload]);
  async function loadOlder() {
    if (next === null || loading) return;
    const request = epoch.current;
    setLoading(true); setError("");
    try {
      const result = await api(`${endpoint}?before_version=${next}`);
      if (request !== epoch.current) return;
      setRows(current=>[...current,...result.versions]); setNext(result.next_before_version);
      setLatest(result.current_version);
    } catch (e:any) { if (request === epoch.current) setError(e.message); }
    finally { if (request === epoch.current) setLoading(false); }
  }
  const row = rows.find(item=>item.version === selected);
  const content = row ? contentOf(row) : "";
  return <Disclosure className="policyHistory" open={open} onOpenChange={setOpen}>
    <DisclosureTrigger>Version history</DisclosureTrigger>
    <DisclosureContent>
      <section aria-label={`${title} version history`}>
        <p>Saved versions are read-only. Browsing history leaves your draft and active settings unchanged.</p>
        {kind === "criteria" && <p className="policyHistoryHint">Version numbers follow verification settings. Some versions may contain the same criteria text.</p>}
        {latest > currentVersion && <p role="status">A newer saved version v{latest} is available. Comparison uses v{currentVersion} loaded in this editor.</p>}
        {error && <p role="alert">{error} <Button type="button" variant="outline" onClick={()=>setReload(value=>value+1)}>Retry history</Button></p>}
        {loading && <p role="status">Loading saved versions…</p>}
        {!loading && !error && !rows.length && <p>No saved versions yet. Defaults and unsaved drafts are not part of version history.</p>}
        {rows.length > 0 && <>
          <Label className="policyHistoryChoice">Saved version
            <NativeSelect aria-label={`${title} saved version`} value={selected ?? ""} onChange={e=>setSelected(Number(e.target.value))}>
              {rows.map(item=><option key={item.version} value={item.version}>v{item.version}{item.version === latest ? " · Current" : ""} · {savedTime(item.updated_at)} · {item.actor || "Actor not recorded"}</option>)}
            </NativeSelect>
          </Label>
          {next !== null && <Button type="button" variant="outline" disabled={loading} onClick={loadOlder}>Load older versions</Button>}
        </>}
        {row && <>
          <p className="policyHistoryMetadata">Saved by {row.actor || "Actor not recorded"} · <time dateTime={row.updated_at || undefined}>{savedTime(row.updated_at)}</time></p>
          <Button type="button" variant="outline" aria-pressed={compare} onClick={()=>setCompare(value=>!value)}>{compare ? "Hide comparison" : "Compare with current saved version"}</Button>
          {compare && <p>{content === currentContent ? "Text matches the saved version loaded in this editor." : "Text differs from the saved version loaded in this editor."}</p>}
          <div className={`policyHistoryContents${compare ? " isComparing" : ""}`}>
            <section aria-label={`${title} historical content`}><h4>Saved v{row.version}</h4><pre tabIndex={0}>{content || "No criteria text was saved in this version."}</pre></section>
            {compare && <section aria-label={`${title} current saved content`}><h4>Saved v{currentVersion} · loaded in editor</h4><pre tabIndex={0}>{currentContent || "No criteria text is saved."}</pre></section>}
          </div>
        </>}
      </section>
    </DisclosureContent>
  </Disclosure>;
}
