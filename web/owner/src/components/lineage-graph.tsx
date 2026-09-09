import React from "react";
import { Button } from "./ui/button";
import { claimDisplayTitle } from "./claim-display";

export function LineageGraph({receipt, available, evidenceNames, selection, onSelect}: any) {
  const [limit, setLimit] = React.useState(3);
  React.useEffect(() => setLimit(3), [receipt.claim.id]);
  const evidence = (receipt.evidence || []).slice(0,limit);
  const height = Math.max(360, evidence.length * 138 + 80);
  const center = height / 2;
  const tone = available ? "admitted" : receipt.state === "needs_revision" ? "revision" : ["rejected", "blocked"].includes(receipt.state) ? "excluded" : "pending";
  const applicability = receipt.claim.applicability || {};
  const boundary = receipt.claim.scope || applicability.title || applicability.description || "No reuse boundary recorded";
  const contextTitle = receipt.claim.scope ? `Scope: ${receipt.claim.scope}` : boundary;
  const node = (id:string, x:number, y:number, title:string, label:string, meta:string, kind:string) => <button key={id} className={`graphNode ${kind}`} style={{left:`${x/920*100}%`,top:y}} aria-pressed={selection === id} onClick={() => onSelect(id)}><small>{label}</small><strong>{title}</strong><span>{meta}</span></button>;
  return <div className="lineageDiagram">
    <div className="graphScroll" tabIndex={0} aria-label="Lineage: evidence, claim, and governed context">
      <div className="graphPlane" style={{"--graph-height": `${height}px`} as React.CSSProperties}>
        <div className="graphColumns"><span>Bound evidence</span><span>Claim</span><span>Governed context</span></div>
        <svg width="100%" height={height} viewBox={`0 0 920 ${height}`} preserveAspectRatio="none" aria-hidden="true">{evidence.map((_:any,i:number) => <path key={i} d={`M 262 ${134+i*138} C 305 ${134+i*138}, 295 ${center}, 338 ${center}`} />)}<path className={available ? "" : tone} d={`M 582 ${center} C 620 ${center}, 622 ${center}, 662 ${center}`} /></svg>
        {evidence.map((e:any,i:number) => node(`evidence:${i}`,18,80+i*138,evidenceNames[i],"Evidence", e.id || e.evidence?.id || `Source ${i+1}`,"evidence"))}
        {!evidence.length && <p className="graphNoEvidence">No bound evidence</p>}
        {node("claim",338,center-70,claimDisplayTitle(receipt.claim),receipt.state.replaceAll("_"," "),[boundary, receipt.claim.created_at && new Date(receipt.claim.created_at).toLocaleString()].filter(Boolean).join(" · "),`claim ${tone}`)}
        {node("context",662,center-70,available ? contextTitle : receipt.state === "admitted" ? "Not eligible in this view" : `Not reusable: ${receipt.state.replaceAll("_"," ")}`,"Reuse boundary", available ? `Approved by ${receipt.review?.reviewer || "actor not recorded"}` : Object.entries(receipt.evaluation?.checks || {}).filter(([,ok])=>!ok).map(([name])=>name.replaceAll("_"," ")).join(", ") || (receipt.state === "admitted" ? "Check actor eligibility" : "Human approval required"),`context ${tone}`)}
      </div>
    </div>
    {receipt.evidence?.length > limit && <Button variant="outline" onClick={() => setLimit(limit+3)}>Show {Math.min(3,receipt.evidence.length-limit)} more sources</Button>}
  </div>;
}
