import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./components/governance.css";
import "./components/knowledge-library.css";
import "./components/ui/component-theme.css";
import { KnowledgeLibrary } from "./components/knowledge-library";
import { Button } from "./components/ui/button";
import { Activity, BookOpen, Home, KeyRound, ShieldCheck } from "./components/ui/icon";

const seedRows = [
  {id:"clm-a", type:"claim", state:"admitted", title:"Evaluation retains the sealed split", label:"Benchmark conclusions remain bounded to the recorded dataset and split.", created_at:"2026-09-18", applicability:{title:"Evaluation protocol",description:"Use when comparing results produced by the same sealed evaluation protocol."}},
  {id:"clm-b", type:"claim", state:"admitted", title:"Calibration uses provider probabilities", label:"Calibration calculations use probabilities rather than provider confidence labels.", created_at:"2026-09-18", applicability:{title:"Evaluation protocol",description:"Use for calibration analysis tied to the recorded provider response."}},
  {id:"clm-c", type:"claim", state:"admitted", title:"Human approval authorizes reuse", label:"Automated checks and model advice remain inputs to the owner decision.", created_at:"2026-09-19", applicability:{title:"Authority boundary",description:"Use when deciding whether agent-produced knowledge may enter downstream context."}},
  {id:"clm-d", type:"claim", state:"admitted", title:"Downstream context excludes stale dependencies", label:"A withdrawn upstream claim blocks declared dependents from governed context.", created_at:"2026-09-20", applicability:{title:"Authority boundary",description:"Use when a declared upstream dependency changes or is withdrawn."}},
];
const additionalTitles = [
  "Provider responses retain model identity",
  "Evaluation retries preserve the original prompt",
  "Sensitive evidence stays outside model input",
  "Policy changes require an owner receipt",
  "Expired evidence pauses downstream reuse",
  "Reproposals retain the rejected predecessor",
  "Retrieval records the selection reason",
  "Agent credentials remain workspace scoped",
  "Human decisions record the ledger head",
  "Relation citations bind a quoted span",
  "Batch judgments preserve per-claim results",
  "Context reads emit consumption receipts",
  "Superseded claims remain auditable",
  "Deterministic failures block model overrides",
  "Task ranking follows eligibility filtering",
  "Withdrawal preserves prior approval history",
];
const topics = ["Evaluation protocol", "Authority boundary", "Evidence handling", "Operations"];
const extraRows = additionalTitles.map((title, index) => ({
  id:`clm-${String.fromCharCode(101 + index)}`,
  type:"claim",
  state:"admitted",
  title,
  label:`Synthetic preview claim ${index + 5}, included to test progressive graph disclosure.`,
  created_at:`2026-09-${String(4 + index).padStart(2,"0")}`,
  applicability:{title:topics[index % topics.length],description:"Synthetic applicability used only for local density testing."},
}));
const rows = [...seedRows, ...extraRows];
const seedNodes = [
  {id:"ev-a",label:"Sealed evaluation manifest"},{id:"ev-b",label:"Calibration result receipt"},{id:"ev-c",label:"Admission policy v1"},{id:"ev-d",label:"Dependency invalidation tests"},
];
const extraNodes = extraRows.map((_, index) => ({id:`ev-${String.fromCharCode(101 + index)}`,label:`Synthetic evidence receipt ${index + 5}`}));
const nodes = [...seedNodes, ...extraNodes];
const seedEdges = [
  {from:"ev-a",to:"clm-a",type:"supports"},{from:"ev-b",to:"clm-b",type:"supports"},{from:"ev-c",to:"clm-c",type:"supports"},{from:"ev-d",to:"clm-d",type:"supports"},
];
const edges = [...seedEdges, ...extraRows.map((row, index) => ({from:extraNodes[index].id,to:row.id,type:"supports"}))];
const seedRelations = [
  {id:"rel-a",from:"clm-b",to:"clm-a",type:"depends_on",state:"admitted",qualifiers:{citation:{evidence_ref:"ev-b"}},advice:{recommendation:"accept",model:"jev-preview"}},
  {id:"rel-b",from:"clm-d",to:"clm-c",type:"qualifies",state:"unresolved",qualifiers:{citation:{evidence_ref:"ev-d"}},advice:{recommendation:"escalate",model:"jev-preview"}},
];
const extraRelations = extraRows.map((row, index) => ({
  id:`rel-${index + 3}`,
  from:row.id,
  to:index ? extraRows[index - 1].id : "clm-d",
  type:index % 3 === 0 ? "qualifies" : "depends_on",
  state:"admitted",
  qualifiers:{citation:{evidence_ref:extraNodes[index].id}},
  advice:{recommendation:"accept",model:"jev-preview"},
}));
const relations = [...seedRelations, ...extraRelations];

const receipts = Object.fromEntries(rows.map((row, index) => [row.id, {
  state:"admitted",
  claim:{id:row.id,title:row.title,statement:row.label,evidence_refs:[`ev-${String.fromCharCode(97 + index)}`],scope:"local-preview",proposer:"agent:local-preview",created_at:row.created_at,applicability:row.applicability},
  evidence:[{id:`ev-${String.fromCharCode(97 + index)}`,quote:nodes[index].label}],
  review:{reviewer:"human:local-owner",created_at:"2026-09-20"},
  history:[],
}]));

function Preview() {
  const [selected, setSelected] = React.useState("");
  const nav = [["Home",Home],["Review",ShieldCheck],["Knowledge",BookOpen],["Runs",Activity],["Activity",Activity],["Admin",KeyRound]] as const;
  return <div className="shell">
    <aside className="sidebar">
      <div className="brand"><span className="brandMark"><img src="/logo.svg" alt="" /></span><strong>Proofpress</strong></div>
      <nav aria-label="Workspace navigation">{nav.map(([label,Icon]) => <Button key={label} variant="ghost" size="content" className={label === "Knowledge" ? "active" : ""} aria-current={label === "Knowledge" ? "page" : undefined}><Icon /><span>{label}</span>{label === "Review" && <em>2</em>}</Button>)}</nav>
      <div className="workspace"><span>WORKSPACE</span><b>Local preview</b><small>Single-owner governance</small></div>
    </aside>
    <main>
      <header className="topbar"><div className="mobileBrand"><span className="brandMark"><img src="/logo.svg" alt="" /></span><strong>Proofpress</strong></div><span className="workspaceLabel"><span className="workspaceContext">Local preview · </span>Knowledge</span><Button variant="outline" disabled>Sign out</Button></header>
      <section className="stage"><p className="previewNotice">Synthetic local preview · no production knowledge</p><KnowledgeLibrary rows={rows} allRows={rows} nodes={nodes} edges={edges} relations={relations} selected={selected} receipt={selected ? receipts[selected] : null} loading={false} contextError="" detailError="" initialView="map" onChoose={setSelected} onReview={()=>{}} evidenceName={(row:any)=>row.quote || row.id} renderEvidence={(row:any)=><p>{row.quote}</p>} /></section>
    </main>
  </div>;
}

createRoot(document.getElementById("root")!).render(<Preview />);
