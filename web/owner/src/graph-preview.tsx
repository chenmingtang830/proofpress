import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./components/governance.css";
import "./components/knowledge-library.css";
import "./components/ui/component-theme.css";
import { KnowledgeLibrary } from "./components/knowledge-library";
import { Button } from "./components/ui/button";
import { Activity, BookOpen, Home, KeyRound, ShieldCheck } from "./components/ui/icon";

const rows = [
  {id:"clm-a", type:"claim", state:"admitted", title:"Evaluation retains the sealed split", label:"Benchmark conclusions remain bounded to the recorded dataset and split.", created_at:"2026-09-18", applicability:{title:"Evaluation protocol",description:"Use when comparing results produced by the same sealed evaluation protocol."}},
  {id:"clm-b", type:"claim", state:"admitted", title:"Calibration uses provider probabilities", label:"Calibration calculations use probabilities rather than provider confidence labels.", created_at:"2026-09-18", applicability:{title:"Evaluation protocol",description:"Use for calibration analysis tied to the recorded provider response."}},
  {id:"clm-c", type:"claim", state:"admitted", title:"Human approval authorizes reuse", label:"Automated checks and model advice remain inputs to the owner decision.", created_at:"2026-09-19", applicability:{title:"Authority boundary",description:"Use when deciding whether agent-produced knowledge may enter downstream context."}},
  {id:"clm-d", type:"claim", state:"admitted", title:"Downstream context excludes stale dependencies", label:"A withdrawn upstream claim blocks declared dependents from governed context.", created_at:"2026-09-20", applicability:{title:"Authority boundary",description:"Use when a declared upstream dependency changes or is withdrawn."}},
];
const nodes = [
  {id:"ev-a",label:"Sealed evaluation manifest"},{id:"ev-b",label:"Calibration result receipt"},{id:"ev-c",label:"Admission policy v1"},{id:"ev-d",label:"Dependency invalidation tests"},
];
const edges = [
  {from:"ev-a",to:"clm-a",type:"supports"},{from:"ev-b",to:"clm-b",type:"supports"},{from:"ev-c",to:"clm-c",type:"supports"},{from:"ev-d",to:"clm-d",type:"supports"},
];
const relations = [
  {id:"rel-a",from:"clm-b",to:"clm-a",type:"depends_on",state:"admitted",qualifiers:{citation:{evidence_ref:"ev-b"}},advice:{recommendation:"accept",model:"jev-preview"}},
  {id:"rel-b",from:"clm-d",to:"clm-c",type:"qualifies",state:"unresolved",qualifiers:{citation:{evidence_ref:"ev-d"}},advice:{recommendation:"escalate",model:"jev-preview"}},
];

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
