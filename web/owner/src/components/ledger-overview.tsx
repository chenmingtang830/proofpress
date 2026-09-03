import React from "react";
import { Button } from "./ui/button";

/** Bounded graph projection. Selecting evidence highlights its real support edges. */
export function LedgerOverview({rows, nodes, edges, onChoose}: any) {
  const [limit, setLimit] = React.useState(6);
  const [sourceLimit, setSourceLimit] = React.useState(12);
  const [scope, setScope] = React.useState("");
  const [source, setSource] = React.useState<string|null>(null);
  const scopes = [...new Set(rows.map((r:any) => r.scope || "Workspace"))] as string[];
  const filtered = rows.filter((r:any) => !scope || (r.scope || "Workspace") === scope);
  const shown = filtered.slice(0,limit);
  const ids = new Set(shown.map((r:any) => r.id));
  const support = edges.filter((e:any) => e.type === "supports" && ids.has(e.to) && !rows.some((r:any) => r.id === e.from));
  const sources = [...new Set(support.map((e:any) => e.from))].slice(0,sourceLimit) as string[];
  const height = Math.max(320,Math.max(sources.length,shown.length)*126+70);
  const related = (id:string) => !source || support.some((e:any) => e.from === source && e.to === id);
  if (!rows.length) return <p className="emptyState">No conclusions in this view.</p>;
  return <div className="globalLineage">
    <div className="globalToolbar"><label>Scope <select value={scope} onChange={e=>{setScope(e.target.value);setLimit(6);setSourceLimit(12);setSource(null);}}><option value="">All scopes</option>{scopes.map(s=><option key={s}>{s}</option>)}</select></label><span>{filtered.length} conclusions in this view</span>{source && <Button variant="outline" onClick={()=>setSource(null)}>Clear evidence selection</Button>}</div>
    <div className="graphScroll" tabIndex={0} aria-label="Global evidence and conclusion graph">
      <div className="globalGraph" style={{height}}>
        <div className="globalColumns"><span>Evidence</span><span>Conclusions</span></div>
        <svg width="100%" height={height} viewBox={`0 0 920 ${height}`} preserveAspectRatio="none" aria-hidden="true">{support.filter((e:any)=>sources.includes(e.from)).map((e:any,i:number)=>{
          const y1=114+sources.indexOf(e.from)*126,y2=114+shown.findIndex((r:any)=>r.id===e.to)*126;
          return <path key={i} className={source===e.from ? "selectedEdge" : ""} style={{opacity:source && source!==e.from ? .2:1}} d={`M 350 ${y1} C 450 ${y1},470 ${y2},570 ${y2}`} />;
        })}</svg>
        {sources.map((id,i)=>{const n=nodes.find((n:any)=>n.id===id);return <button key={id} className="globalNode source" style={{top:64+i*126}} aria-pressed={source===id} onClick={()=>setSource(source===id?null:id)}><strong>{n?.label || id}</strong><small>{id} · {support.filter((e:any)=>e.from===id).length} linked conclusions</small></button>;})}
        {shown.map((r:any,i:number)=><button key={r.id} className="globalNode conclusionNode" data-state={r.state} style={{top:64+i*126,opacity:related(r.id)?1:.35}} onClick={()=>onChoose(r.id)}><small>{r.state.replaceAll("_"," ")} · {r.scope || "Workspace"}</small><strong>{r.label}</strong></button>)}
      </div>
    </div>
    <div className="globalToolbar">{filtered.length>limit && <Button variant="outline" onClick={()=>setLimit(limit+6)}>Show more conclusions</Button>}{new Set(support.map((e:any)=>e.from)).size>sourceLimit && <Button variant="outline" onClick={()=>setSourceLimit(sourceLimit+12)}>Show more evidence</Button>}</div>
  </div>;
}
