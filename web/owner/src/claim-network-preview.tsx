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
const dateBands = ["Sep 04 · 2026","Sep 09 · 2026","Sep 14 · 2026","Sep 20 · 2026"];
const lines = (value:string,maxChars = 21,maxLines = 3) => {
  const words = value.split(" ");
  const output:string[] = [""];
  for (const word of words) {
    const next = `${output[output.length - 1]} ${word}`.trim();
    if (next.length > maxChars && output.length < maxLines) output.push(word);
    else if (next.length > maxChars) output[output.length - 1] = `${output[output.length - 1].replace(/…$/,"")}…`;
    else output[output.length - 1] = next;
  }
  return output;
};

function ClaimNetwork() {
  const [nodeLimit, setNodeLimit] = React.useState(8);
  const [edgeLimit, setEdgeLimit] = React.useState(8);
  const [selected, setSelected] = React.useState("clm-c");
  const [showEvidence, setShowEvidence] = React.useState(false);
  const [openReceipt, setOpenReceipt] = React.useState<string | null>(null);
  const [query, setQuery] = React.useState("");
  const selectedClaim = claimById(selected);
  const visibleClaims = claims.slice(0,nodeLimit).filter(claim => !query || `${claim.title} ${claim.statement}`.toLowerCase().includes(query.toLowerCase()));
  const visibleIds = new Set(visibleClaims.map(claim => claim.id));
  const availableRelations = relations.filter(relation => visibleIds.has(relation.from) && visibleIds.has(relation.to));
  const visibleRelations = availableRelations.slice(0,edgeLimit);
  const selectedRelations = relations.filter(relation => relation.from === selected || relation.to === selected);
  const neighbors = relations.filter(relation => relation.from === selected || relation.to === selected).map(relation => relation.from === selected ? relation.to : relation.from);
  const rowCount = Math.ceil(nodeLimit / dateBands.length);
  const positions = new Map(visibleClaims.map(claim => {
    const index = claims.findIndex(item => item.id === claim.id);
    const column = index % dateBands.length;
    const row = Math.floor(index / dateBands.length);
    const y = rowCount === 2 ? 220 + row * 210 : rowCount === 3 ? 145 + row * 170 : 95 + row * 110;
    return [claim.id,{x:[120,340,560,780][column],y}] as const;
  }));
  const visibleSelectedClaim = visibleIds.has(selected) ? selectedClaim : null;
  const selectClaim = (id:string) => { setSelected(id); setShowEvidence(false); setOpenReceipt(null); };
  const updateQuery = (value:string) => {
    setQuery(value);
    const firstMatch = claims.slice(0,nodeLimit).find(claim => `${claim.title} ${claim.statement} ${claim.topic} ${claim.evidence.join(" ")}`.toLowerCase().includes(value.toLowerCase()));
    if (firstMatch && firstMatch.id !== selected) selectClaim(firstMatch.id);
  };
  const reset = () => { setNodeLimit(initialScene.length); setEdgeLimit(8); setSelected("clm-c"); setShowEvidence(false); setOpenReceipt(null); setQuery(""); };
  return <section className="networkPage">
    <header className="networkHead">
      <div><h1>Claim network</h1><p>Explore admitted claims and their recorded relationships.</p></div>
      <div className="networkCount"><strong>{visibleClaims.length}</strong><span>claims · {visibleRelations.length} relations</span></div>
    </header>
    <div className="networkToolbar">
      <Label>Find claims<Input type="search" value={query} onChange={event => updateQuery(event.target.value)} placeholder="Search statements, scope, or evidence…" /></Label>
      <Label>Nodes<NativeSelect value={nodeLimit} onChange={event => { const next = Number(event.target.value); setNodeLimit(next); if (claims.findIndex(claim => claim.id === selected) >= next) selectClaim(claims[0].id); }}><option value="8">8 claims</option><option value="12">12 claims</option><option value="20">20 claims</option></NativeSelect></Label>
      <Label>Edges<NativeSelect value={edgeLimit} onChange={event => setEdgeLimit(Number(event.target.value))}><option value="4">Up to 4</option><option value="8">Up to 8</option><option value="18">All relations</option></NativeSelect></Label>
      <Button variant="outline" className="h-10" onClick={reset}>Reset scene</Button>
    </div>
    <div className="networkWorkspace">
      <div className="networkCanvas" aria-label="Interactive claim network">
        <svg viewBox="0 0 900 630" role="img" aria-label={`${visibleClaims.length} admitted claims and ${visibleRelations.length} relationships`}>
          <defs><marker id="networkArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" /></marker></defs>
          {dateBands.map((date,index) => <g className="networkDate" key={date}><text x={[120,340,560,780][index]} y="32" textAnchor="middle">{date}</text><line x1={[120,340,560,780][index]} y1="48" x2={[120,340,560,780][index]} y2="602"/></g>)}
          {visibleRelations.map(relation => {
            const from = positions.get(relation.from), to = positions.get(relation.to); if (!from || !to) return null;
            const active = relation.from === selected || relation.to === selected;
            const mx = (from.x + to.x) / 2, my = (from.y + to.y) / 2;
            const path = from.x === to.x ? `M${from.x} ${from.y} C${from.x + 70} ${from.y},${to.x + 70} ${to.y},${to.x} ${to.y}` : `M${from.x} ${from.y} C${mx} ${from.y},${mx} ${to.y},${to.x} ${to.y}`;
            return <g key={relation.id} className={`networkEdge${active ? " active" : ""}${relation.state === "unresolved" ? " unresolved" : ""}`}>
              <path d={path} markerEnd="url(#networkArrow)" />
              {active && <text x={mx} y={my - 8} textAnchor="middle">{relation.type}</text>}
            </g>;
          })}
          {visibleClaims.map(claim => {
            const position = positions.get(claim.id)!; const active = claim.id === selected;
            const radius = nodeLimit === 20 ? 38 : nodeLimit === 12 ? 50 : 62;
            const lineHeight = nodeLimit === 20 ? 12 : 16;
            const labelLines = lines(claim.title,nodeLimit === 20 ? 15 : 21,nodeLimit === 20 ? 2 : 3);
            const labelStart = position.y - ((labelLines.length - 1) * lineHeight) / 2 + 7;
            return <g key={claim.id} data-claim-id={claim.id} className={`networkNode${active ? " selected" : ""}`} role="button" tabIndex={0} focusable="true" aria-label={claim.title} aria-pressed={active} onClick={() => selectClaim(claim.id)} onKeyDown={event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectClaim(claim.id); } }}>
              <title>{claim.title}</title>
              {active && <circle className="networkSelectionRing" cx={position.x} cy={position.y} r={radius + 7}/>}
              <circle className="networkNodeBody" cx={position.x} cy={position.y} r={radius}/>
              <text className="networkTopic" x={position.x} y={position.y - radius * .48} textAnchor="middle">Claim</text>
              {labelLines.map((line,index) => <text className="networkTitle" key={`${line}-${index}`} x={position.x} y={labelStart + index * lineHeight} textAnchor="middle">{line}</text>)}
            </g>;
          })}
        </svg>
        <div className="networkMobileTimeline" aria-label="Claims by recorded date">
          <h2>Claims by recorded date</h2>
          {dateBands.map((date,column) => {
            const datedClaims = visibleClaims.filter(claim => claims.findIndex(item => item.id === claim.id) % dateBands.length === column);
            if (!datedClaims.length) return null;
            return <section key={date}><h3>{date}</h3>{datedClaims.map(claim => { const relationCount = relations.filter(relation => relation.from === claim.id || relation.to === claim.id).length; return <Button key={claim.id} variant="ghost" size="content" className={claim.id === selected ? "selected" : ""} aria-pressed={claim.id === selected} onClick={() => selectClaim(claim.id)}><span>{claim.title}</span><small>{claim.evidence.length} evidence · {relationCount} {relationCount === 1 ? "relation" : "relations"}</small></Button>; })}</section>;
          })}
        </div>
        <ul className="sr-only" aria-label="Claims shown in graph">{visibleClaims.map(claim => <li key={claim.id}><Button variant="ghost" size="content" aria-pressed={claim.id === selected} onClick={() => selectClaim(claim.id)}>{claim.title}</Button></li>)}</ul>
        <ul className="sr-only" aria-label="Relationships shown in graph">{visibleRelations.map(relation => <li key={relation.id}>{claimById(relation.from).title} {relation.type} {claimById(relation.to).title}. {relation.state === "admitted" ? "Recorded relation" : "Unresolved relation"}.</li>)}</ul>
        {!visibleClaims.length && <div className="networkEmpty"><strong>No matching claims</strong><span>Clear or change the search.</span></div>}
      </div>
      <aside className="networkSidecar">
        <p className="sr-only" aria-live="polite">{visibleSelectedClaim ? `Selected claim: ${visibleSelectedClaim.title}` : "No matching claim selected"}</p>
        {!visibleSelectedClaim ? <div className="networkSidecarEmpty"><h2>No matching claim</h2><p>Change or clear the search to inspect a claim.</p></div> : openReceipt ? <>
          <div className="networkReceiptNav"><Button variant="ghost" size="content" className="networkBack" onClick={() => setOpenReceipt(null)}>Back to claim</Button></div>
          <small>Evidence receipt</small><h2>{openReceipt}</h2><p>Recorded support bound to this claim. Synthetic preview only.</p>
          <dl><div><dt>Receipt</dt><dd>{`rec-${selected}-${String(visibleSelectedClaim.evidence.indexOf(openReceipt) + 1).padStart(2,"0")}`}</dd></div><div><dt>Recorded</dt><dd>{dateBands[claims.findIndex(claim => claim.id === selected) % dateBands.length]}</dd></div><div><dt>Bound to</dt><dd>{visibleSelectedClaim.title}</dd></div></dl>
          <section className="networkReceiptExcerpt"><h3>Recorded excerpt</h3><p>{openReceipt} supports “{visibleSelectedClaim.title}”.</p></section>
        </> : <>
          <small>Admitted claim</small><h2>{visibleSelectedClaim.title}</h2><p>{visibleSelectedClaim.statement}</p>
          <dl><div><dt>Recorded</dt><dd>{dateBands[claims.findIndex(claim => claim.id === selected) % dateBands.length]}</dd></div><div><dt>Scope</dt><dd>{visibleSelectedClaim.topic}</dd></div><div><dt>Relationships</dt><dd>{neighbors.length}</dd></div><div><dt>Evidence</dt><dd>{visibleSelectedClaim.evidence.length} receipts</dd></div></dl>
          <section className="networkRelationList"><h3>Relationships</h3>{selectedRelations.map(relation => { const otherId = relation.from === selected ? relation.to : relation.from; return <Button key={relation.id} variant="ghost" size="content" onClick={() => selectClaim(otherId)}><span><b>{relation.type}</b> {claimById(otherId).title}</span><small>{relation.state === "admitted" ? "Recorded" : "Unresolved"}</small></Button>; })}</section>
          <div className="networkActions"><Button variant="outline" onClick={() => setShowEvidence(value => !value)}>{showEvidence ? "Hide evidence" : "Show evidence"}</Button></div>
          {showEvidence && <section className="networkEvidenceList"><h3>Bound evidence</h3>{visibleSelectedClaim.evidence.map(item => <Button key={item} variant="ghost" size="content" className="networkReceiptButton" onClick={() => setOpenReceipt(item)}><span>{item}</span><span>Open receipt</span></Button>)}</section>}
        </>}
      </aside>
    </div>
    <footer className="networkHint"><span className="networkLegend"><i className="recorded"/>Recorded relation <i className="unresolved"/>Unresolved</span><span>Recorded time runs left to right.</span></footer>
  </section>;
}

function Preview() {
  const nav = [["Home",Home],["Review",ShieldCheck],["Knowledge",BookOpen],["Runs",Activity],["Activity",Activity],["Admin",KeyRound]] as const;
  return <div className="shell"><aside className="sidebar"><div className="brand"><span className="brandMark"><img src="/logo.svg" alt="" /></span><strong>Proofpress</strong></div><nav aria-label="Workspace navigation">{nav.map(([label,Icon]) => <Button key={label} variant="ghost" size="content" className={label === "Knowledge" ? "active" : ""}><Icon/><span>{label}</span></Button>)}</nav><div className="workspace"><span>WORKSPACE</span><b>Local prototype</b><small>Synthetic claims</small></div></aside><main><header className="topbar"><span className="workspaceLabel">Local prototype · Knowledge</span><Button variant="outline" disabled>Sign out</Button></header><section className="stage networkStage"><div className="networkFrame"><p className="networkNotice">Synthetic prototype · no production knowledge</p><ClaimNetwork/></div></section></main></div>;
}

createRoot(document.getElementById("root")!).render(<Preview/>);
