import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./claim-network-preview.css";
import "./components/ui/component-theme.css";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { NativeSelect } from "./components/ui/native-select";
import { Activity, BookOpen, Home, KeyRound, ShieldCheck } from "./components/ui/icon";

type Claim = {id:string; title:string; topic:string; statement:string; evidence:string[]};
type Relation = {id:string; from:string; to:string; type:string; state:"admitted"|"unresolved"};

const claims: Claim[] = [
  {id:"clm-a",title:"Evaluation retains the sealed split",topic:"Evaluation",statement:"Benchmark conclusions remain bounded to the recorded dataset and split.",evidence:["Sealed evaluation manifest","Dataset revision receipt"]},
  {id:"clm-b",title:"Calibration uses provider probabilities",topic:"Evaluation",statement:"Calibration uses probabilities rather than provider confidence labels.",evidence:["Calibration result receipt"]},
  {id:"clm-c",title:"Human approval authorizes reuse",topic:"Authority",statement:"Checks and model advice remain inputs to the owner decision.",evidence:["Admission policy v1"]},
  {id:"clm-d",title:"Stale dependencies pause downstream reuse",topic:"Authority",statement:"A changed upstream claim pauses declared dependents until reassessment.",evidence:["Dependency invalidation tests"]},
  {id:"clm-e",title:"Provider responses retain model identity",topic:"Evidence",statement:"Each provider response records the requested and returned model identity.",evidence:["Provider response receipt"]},
  {id:"clm-f",title:"Sensitive evidence stays outside model input",topic:"Evidence",statement:"Private source material is projected into a bounded citation before judgment.",evidence:["Redaction policy","Citation projection"]},
  {id:"clm-g",title:"Policy changes require an owner receipt",topic:"Authority",statement:"A policy draft is inactive until the owner records activation.",evidence:["Policy activation receipt"]},
  {id:"clm-h",title:"Expired evidence pauses downstream reuse",topic:"Lifecycle",statement:"Expiry preserves history while removing the claim from current reuse.",evidence:["Expiry evaluation"]},
  {id:"clm-i",title:"Reproposals retain the rejected predecessor",topic:"Lifecycle",statement:"Corrected claims reference the immutable rejected candidate.",evidence:["Reproposal lineage receipt"]},
  {id:"clm-j",title:"Retrieval records the selection reason",topic:"Evidence",statement:"Every retrieval receipt states why the evidence was selected.",evidence:["Retrieval receipt"]},
  {id:"clm-k",title:"Agent credentials remain workspace scoped",topic:"Access",statement:"Agent credentials do not grant cross-workspace visibility.",evidence:["Credential policy"]},
  {id:"clm-l",title:"Human decisions record the ledger head",topic:"Authority",statement:"Owner decisions bind the expected append-only ledger head.",evidence:["Decision receipt"]},
  {id:"clm-m",title:"Relation citations bind a quoted span",topic:"Relations",statement:"A proposed relationship identifies its supporting evidence quote.",evidence:["Relation citation receipt"]},
  {id:"clm-n",title:"Context reads emit consumption receipts",topic:"Operations",statement:"Governed-context retrieval records what was returned without proving use.",evidence:["Context read receipt"]},
  {id:"clm-o",title:"Superseded claims remain auditable",topic:"Lifecycle",statement:"Replacement removes current reuse without erasing prior authority.",evidence:["Supersession event"]},
  {id:"clm-p",title:"Deterministic failures block model overrides",topic:"Evaluation",statement:"Advisory acceptance cannot override a failed deterministic gate.",evidence:["Evaluation policy v2"]},
  {id:"clm-q",title:"Task ranking follows eligibility filtering",topic:"Operations",statement:"Ranking happens only after authority and actor eligibility filters.",evidence:["Context selection trace"]},
  {id:"clm-r",title:"Withdrawal preserves approval history",topic:"Lifecycle",statement:"Withdrawal stops reuse while retaining the original human decision.",evidence:["Withdrawal transaction"]},
  {id:"clm-s",title:"Batch judgments preserve claim results",topic:"Evaluation",statement:"Each claim retains its own recommendation and audit packet.",evidence:["Batch judgment receipt"]},
  {id:"clm-t",title:"Relations require independent admission",topic:"Relations",statement:"Admitted claims do not automatically admit a proposed relationship.",evidence:["Relation review receipt"]},
];

const relations: Relation[] = [
  {id:"r1",from:"clm-b",to:"clm-a",type:"depends on",state:"admitted"},
  {id:"r2",from:"clm-d",to:"clm-c",type:"qualifies",state:"unresolved"},
  {id:"r3",from:"clm-e",to:"clm-b",type:"supports",state:"admitted"},
  {id:"r4",from:"clm-f",to:"clm-e",type:"qualifies",state:"admitted"},
  {id:"r5",from:"clm-g",to:"clm-c",type:"depends on",state:"admitted"},
  {id:"r6",from:"clm-h",to:"clm-d",type:"supports",state:"admitted"},
  {id:"r7",from:"clm-i",to:"clm-o",type:"related to",state:"admitted"},
  {id:"r8",from:"clm-j",to:"clm-f",type:"supports",state:"admitted"},
  {id:"r9",from:"clm-k",to:"clm-n",type:"qualifies",state:"admitted"},
  {id:"r10",from:"clm-l",to:"clm-c",type:"supports",state:"admitted"},
  {id:"r11",from:"clm-m",to:"clm-t",type:"depends on",state:"admitted"},
  {id:"r12",from:"clm-n",to:"clm-q",type:"depends on",state:"admitted"},
  {id:"r13",from:"clm-o",to:"clm-r",type:"contrasts",state:"admitted"},
  {id:"r14",from:"clm-p",to:"clm-s",type:"qualifies",state:"admitted"},
  {id:"r15",from:"clm-q",to:"clm-n",type:"same scope",state:"admitted"},
  {id:"r16",from:"clm-r",to:"clm-d",type:"triggers",state:"admitted"},
  {id:"r17",from:"clm-s",to:"clm-a",type:"depends on",state:"admitted"},
  {id:"r18",from:"clm-t",to:"clm-m",type:"qualifies",state:"admitted"},
];

const initialScene = ["clm-a","clm-b","clm-c","clm-d","clm-e","clm-g","clm-l","clm-s"];
const claimById = (id:string) => claims.find(claim => claim.id === id)!;
const lines = (value:string) => {
  const words = value.split(" ");
  const output:string[] = [""];
  for (const word of words) {
    const next = `${output[output.length - 1]} ${word}`.trim();
    if (next.length > 21 && output.length < 3) output.push(word); else output[output.length - 1] = next;
  }
  return output;
};

function ClaimNetwork() {
  const [scene, setScene] = React.useState(initialScene);
  const [selected, setSelected] = React.useState("clm-c");
  const [showEvidence, setShowEvidence] = React.useState(false);
  const [query, setQuery] = React.useState("");
  const [topic, setTopic] = React.useState("");
  const selectedClaim = claimById(selected);
  const visibleClaims = scene.map(claimById).filter(claim => (!topic || claim.topic === topic) && (!query || `${claim.title} ${claim.statement}`.toLowerCase().includes(query.toLowerCase())));
  const visibleIds = new Set(visibleClaims.map(claim => claim.id));
  const visibleRelations = relations.filter(relation => visibleIds.has(relation.from) && visibleIds.has(relation.to));
  const neighbors = relations.filter(relation => relation.from === selected || relation.to === selected).map(relation => relation.from === selected ? relation.to : relation.from);
  const hiddenNeighbors = [...new Set(neighbors.filter(id => !scene.includes(id)))];
  const positions = new Map<string,{x:number;y:number}>();
  const others = visibleClaims.filter(claim => claim.id !== selected);
  if (visibleIds.has(selected)) positions.set(selected,{x:450,y:315});
  others.forEach((claim,index) => {
    const angle = -Math.PI / 2 + index * Math.PI * 2 / Math.max(others.length,1);
    positions.set(claim.id,{x:450 + Math.cos(angle) * 285,y:315 + Math.sin(angle) * 215});
  });
  if (!visibleIds.has(selected)) visibleClaims.forEach((claim,index) => {
    const angle = -Math.PI / 2 + index * Math.PI * 2 / Math.max(visibleClaims.length,1);
    positions.set(claim.id,{x:450 + Math.cos(angle) * 285,y:315 + Math.sin(angle) * 215});
  });
  const selectClaim = (id:string) => { setSelected(id); setShowEvidence(false); };
  const expand = () => setScene(current => [...new Set([...current,...hiddenNeighbors.slice(0,6)])]);
  const reset = () => { setScene(initialScene); setSelected("clm-c"); setShowEvidence(false); setQuery(""); setTopic(""); };
  return <section className="networkPage">
    <header className="networkHead">
      <div><h1>Claim network</h1><p>Explore admitted claims and their recorded relationships.</p></div>
      <div className="networkCount"><strong>{scene.length}</strong><span>of {claims.length} claims in scene</span></div>
    </header>
    <div className="networkToolbar">
      <Label>Find claims<Input type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder="Search claims…" /></Label>
      <Label>Applicability<NativeSelect value={topic} onChange={event => setTopic(event.target.value)}><option value="">All</option>{[...new Set(claims.map(claim => claim.topic))].map(value => <option key={value}>{value}</option>)}</NativeSelect></Label>
      <Button variant="outline" onClick={reset}>Reset scene</Button>
    </div>
    <div className="networkWorkspace">
      <div className="networkCanvas" aria-label="Interactive claim network">
        <svg viewBox="0 0 900 630" role="img" aria-label={`${visibleClaims.length} admitted claims and ${visibleRelations.length} relationships`}>
          <defs><marker id="networkArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" /></marker></defs>
          {visibleRelations.map(relation => {
            const from = positions.get(relation.from), to = positions.get(relation.to); if (!from || !to) return null;
            const active = relation.from === selected || relation.to === selected;
            const mx = (from.x + to.x) / 2, my = (from.y + to.y) / 2;
            return <g key={relation.id} className={`networkEdge${active ? " active" : ""}${relation.state === "unresolved" ? " unresolved" : ""}`}>
              <line x1={from.x} y1={from.y} x2={to.x} y2={to.y} markerEnd="url(#networkArrow)" />
              {active && <text x={mx} y={my - 8} textAnchor="middle">{relation.type}</text>}
            </g>;
          })}
          {showEvidence && selectedClaim.evidence.map((evidence,index) => {
            const x = 450 + (index - (selectedClaim.evidence.length - 1) / 2) * 78, y = 435;
            return <g className="networkEvidence" key={evidence}><line x1="450" y1="315" x2={x} y2={y}/><circle cx={x} cy={y} r="32"/><text x={x} y={y - 3} textAnchor="middle">Evidence</text><text x={x} y={y + 13} textAnchor="middle">{index + 1}</text></g>;
          })}
          {visibleClaims.map(claim => {
            const position = positions.get(claim.id)!; const active = claim.id === selected; const labelLines = lines(claim.title);
            const labelStart = position.y - ((labelLines.length - 1) * 16) / 2 + 7;
            return <g key={claim.id} data-claim-id={claim.id} className={`networkNode${active ? " selected" : ""}`} role="button" tabIndex={0} focusable="true" aria-label={claim.title} onClick={() => selectClaim(claim.id)} onKeyDown={event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectClaim(claim.id); } }}>
              <title>{claim.title}</title>
              <circle cx={position.x} cy={position.y} r={active ? 72 : 62}/>
              <text className="networkTopic" x={position.x} y={position.y - 30} textAnchor="middle">{claim.topic}</text>
              {labelLines.map((line,index) => <text className="networkTitle" key={line} x={position.x} y={labelStart + index * 16} textAnchor="middle">{line}</text>)}
            </g>;
          })}
        </svg>
        {!visibleClaims.length && <div className="networkEmpty"><strong>No matching claims</strong><span>Clear the search or applicability filter.</span></div>}
      </div>
      <aside className="networkSidecar" aria-live="polite">
        <small>Admitted claim</small><h2>{selectedClaim.title}</h2><p>{selectedClaim.statement}</p>
        <dl><div><dt>Applicability</dt><dd>{selectedClaim.topic}</dd></div><div><dt>Relationships</dt><dd>{neighbors.length}</dd></div><div><dt>Evidence</dt><dd>{selectedClaim.evidence.length} receipts</dd></div></dl>
        <div className="networkActions"><Button variant="default" onClick={expand} disabled={!hiddenNeighbors.length}>Expand neighbors{hiddenNeighbors.length ? ` (${hiddenNeighbors.length})` : ""}</Button><Button variant="outline" onClick={() => setShowEvidence(value => !value)}>{showEvidence ? "Hide evidence" : "Reveal evidence"}</Button><Button variant="ghost" onClick={() => setScene([selected])}>Keep only this claim</Button></div>
        {showEvidence && <section className="networkEvidenceList"><h3>Bound evidence</h3>{selectedClaim.evidence.map(item => <Button key={item} variant="ghost" size="content">{item}<span>Open receipt</span></Button>)}</section>}
      </aside>
    </div>
    <footer className="networkHint"><span>Select a claim to inspect it.</span><span>Expand only when another hop matters.</span></footer>
  </section>;
}

function Preview() {
  const nav = [["Home",Home],["Review",ShieldCheck],["Knowledge",BookOpen],["Runs",Activity],["Activity",Activity],["Admin",KeyRound]] as const;
  return <div className="shell"><aside className="sidebar"><div className="brand"><span className="brandMark"><img src="/logo.svg" alt="" /></span><strong>Proofpress</strong></div><nav aria-label="Workspace navigation">{nav.map(([label,Icon]) => <Button key={label} variant="ghost" size="content" className={label === "Knowledge" ? "active" : ""}><Icon/><span>{label}</span></Button>)}</nav><div className="workspace"><span>WORKSPACE</span><b>Local prototype</b><small>Synthetic claims</small></div></aside><main><header className="topbar"><span className="workspaceLabel">Local prototype · Knowledge</span><Button variant="outline" disabled>Sign out</Button></header><section className="stage"><p className="previewNotice">Claim-first graph prototype · no production knowledge</p><ClaimNetwork/></section></main></div>;
}

createRoot(document.getElementById("root")!).render(<Preview/>);
