import React from "react";
import { Button } from "./ui/button";

export function LineageGraph({receipt, available, evidenceNames, selection, onSelect}: any) {
  const [limit, setLimit] = React.useState(3);
  React.useEffect(() => setLimit(3), [receipt.conclusion.id]);
  const evidence = (receipt.evidence || []).slice(0,limit);
  const height = Math.max(330, evidence.length * 138 + 80);
  const center = height / 2;
  const tone = available ? "admitted" : receipt.state === "needs_revision" ? "revision" : ["rejected", "blocked"].includes(receipt.state) ? "excluded" : "pending";
  const node = (id:string, x:number, y:number, title:string, label:string, meta:string, kind:string) => <button key={id} className={`graphNode ${kind}`} style={{left:`${x/920*100}%`,top:y}} aria-pressed={selection === id} onClick={() => onSelect(id)}><small>{label}</small><strong>{title}</strong><span>{meta}</span></button>;
  return <div className="lineageDiagram">
    <div className="graphScroll" tabIndex={0} aria-label="Lineage graph; scroll horizontally on small screens">
      <div className="graphPlane" style={{height}}>
        <div className="graphColumns"><span>Bound evidence</span><span>Conclusion</span><span>Governed context</span></div>
        <svg width="100%" height={height} viewBox={`0 0 920 ${height}`} preserveAspectRatio="none" aria-hidden="true">{evidence.map((_:any,i:number) => <path key={i} d={`M 262 ${134+i*138} C 305 ${134+i*138}, 295 ${center}, 338 ${center}`} />)}<path className={available ? "" : tone} d={`M 582 ${center} C 620 ${center}, 622 ${center}, 662 ${center}`} /></svg>
        {evidence.map((e:any,i:number) => node(`evidence:${i}`,18,80+i*138,evidenceNames[i],"Evidence", e.id || e.evidence?.id || `Source ${i+1}`,"evidence"))}
        {!evidence.length && <p className="graphNoEvidence">No bound evidence</p>}
        {node("conclusion",338,center-54,receipt.conclusion.statement,receipt.state.replaceAll("_"," "),receipt.conclusion.scope,tone)}
        {node("context",662,center-54,available ? `Scope: ${receipt.conclusion.scope || "Workspace"}` : receipt.state === "admitted" ? "Not eligible in this view" : `Not reusable: ${receipt.state.replaceAll("_"," ")}`,"Reuse boundary", available ? `Approved by ${receipt.review?.reviewer || "actor not recorded"}` : Object.entries(receipt.evaluation?.checks || {}).filter(([,ok])=>!ok).map(([name])=>name.replaceAll("_"," ")).join(", ") || (receipt.state === "admitted" ? "Check scope and actor eligibility" : "Human approval required"),tone)}
      </div>
    </div>
    {receipt.evidence?.length > limit && <Button variant="outline" onClick={() => setLimit(limit+3)}>Show {Math.min(3,receipt.evidence.length-limit)} more sources</Button>}
  </div>;
}
