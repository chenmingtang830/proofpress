import React from "react";
import { Button } from "./ui/button";
import { ChevronRight } from "./ui/icon";
import { LineageGraph } from "./lineage-graph";
import { historyActor } from "./review-feedback";
import { admissionRecord, knowledgeDate, knowledgeTopic, recordedIdentity, selectKnowledge, type KnowledgeRow, type KnowledgeSort } from "./knowledge-model";
import "./knowledge-library.css";

function RecordedList({ values, missing }: { values?: string[]; missing: string }) {
  return values?.length ? <ul>{values.map((value, i) => <li key={i}>{value}</li>)}</ul> : <p className="knowledgeMissing">{missing}</p>;
}

export function KnowledgeRecord({ receipt, onClose, onLineage, renderEvidence, evidenceName }: any) {
  const panel = React.useRef<HTMLElement>(null);
  const close = React.useRef<HTMLButtonElement>(null);
  React.useEffect(() => {
    panel.current?.scrollTo({ top: 0 });
    if (window.matchMedia("(max-width: 1099px)").matches) close.current?.focus();
  }, [receipt.claim.id]);
  const claim = receipt.claim;
  const card = claim.applicability;
  const admission = admissionRecord(receipt);
  const evidence = receipt.evidence || [];
  return <article className="knowledgeRecord" ref={panel} aria-label="Knowledge record" onKeyDown={event => { if (event.key === "Escape") { event.stopPropagation(); onClose(); } }}>
    <div className="knowledgeRecordBar"><span>Claim record</span><button ref={close} type="button" onClick={onClose}>Close record</button></div>
    <div className="knowledgeRecordBody">
      <span className="knowledgeAvailable">Available for reuse</span>
      <p className="knowledgeEligibility">Current for this owner view. Agent access is checked separately.</p>
      <h2>{claim.statement}</h2>
      <dl className="knowledgeAttribution">
        <div><dt>Proposed by</dt><dd>{recordedIdentity(claim.proposer, "Proposer not recorded")}</dd></div>
        <div><dt>Admitted by</dt><dd>{recordedIdentity(admission?.reviewer, "Authorizer not recorded")}{admission?.created_at && <span>{knowledgeDate(admission.created_at)}</span>}</dd></div>
      </dl>
      <section className="knowledgeScope"><h3>May support</h3>
        {card?.description && <p>{card.description}</p>}
        <RecordedList values={card?.when_relevant} missing={card?.description ? "Specific use cases not recorded." : "Permitted uses not recorded. Inspect the evidence and recorded boundary before relying on this claim."} />
        {(card?.title || claim.scope) && <p className="knowledgeBoundary">{card?.title ? "Applicability" : "Legacy scope"}: {card?.title || claim.scope}</p>}
      </section>
      <section className="knowledgeScope"><h3>Limits & conditions</h3><RecordedList values={card?.validity_conditions} missing="No explicit validity conditions recorded. This does not establish unrestricted use." /></section>
      <details className="knowledgeEvidence"><summary>Supporting evidence <span>{evidence.length} {evidence.length === 1 ? "source" : "sources"}</span></summary>
        {evidence.length ? evidence.map((row: any, i: number) => <section key={row.id || i}><h4>{evidenceName(row)}</h4>{renderEvidence(row)}</section>) : <p className="knowledgeMissing">Evidence content is not present in this receipt.{claim.evidence_refs?.length ? ` ${claim.evidence_refs.length} evidence references are recorded.` : ""}</p>}
      </details>
      <details className="knowledgeEvidence"><summary>Admission & history <span>{receipt.history?.length || 0} events</span></summary>
        {admission?.note && <p>{admission.note}</p>}
        <p className="knowledgeMissing">This claim is in the current owner context. Each agent's access is checked separately.</p>
        <ol className="knowledgeHistory">{(receipt.history || []).map((event: any, i: number) => <li key={event.event_id || i}><strong>{String(event.type || "Recorded event").replaceAll("_", " ")}</strong><span>{historyActor({ ...event, reviewer: recordedIdentity(event.reviewer, ""), actor: recordedIdentity(event.actor, ""), verifier: recordedIdentity(event.verifier, ""), judge: recordedIdentity(event.judge, ""), claim: { proposer: recordedIdentity(event.claim?.proposer, "") }, model: typeof event.model === "string" ? event.model : undefined })}</span><time>{knowledgeDate(event.created_at)}</time></li>)}</ol>
        {!receipt.history?.length && <p>History is not present in this receipt.</p>}
      </details>
      <footer className="knowledgeRecordFooter"><Button variant="outline" onClick={onLineage}>View lineage</Button><span className="mono">{claim.id}</span></footer>
    </div>
  </article>;
}

export function KnowledgeLibrary({ rows, allRows, relations, selected, receipt, onChoose, onReview, loading, contextError, detailError, renderEvidence, evidenceName }: any) {
  const [query, setQuery] = React.useState("");
  const [topic, setTopic] = React.useState("");
  const [sort, setSort] = React.useState<KnowledgeSort>("newest");
  const [focused, setFocused] = React.useState(rows.some((row: KnowledgeRow) => row.id === selected));
  const [lineage, setLineage] = React.useState(false);
  const [graphSelection, setGraphSelection] = React.useState("claim");
  const previousSelection = React.useRef(selected);
  const pendingSelection = React.useRef(loading ? selected : null);
  React.useEffect(() => {
    if (previousSelection.current !== selected) { previousSelection.current = selected; pendingSelection.current = selected; }
    if (!loading && pendingSelection.current) {
      setFocused(rows.some((row: KnowledgeRow) => row.id === pendingSelection.current));
      pendingSelection.current = null;
    }
  }, [selected, loading, rows]);
  const topics = [...new Set((rows as KnowledgeRow[]).map(knowledgeTopic).filter(Boolean))].sort();
  const visible = selectKnowledge(rows, query, topic, sort);
  const current = !loading && !contextError && rows.some((row: KnowledgeRow) => row.id === selected) && receipt?.claim.id === selected ? receipt : null;
  const reviewCount = allRows.filter((row: KnowledgeRow) => ["needs_review", "needs_revision", "unresolved"].includes(row.state || "")).length;
  const opener = React.useRef<HTMLElement | null>(null);
  const focus = (id: string, element?: HTMLElement) => { opener.current = element || null; setFocused(true); setGraphSelection("claim"); onChoose(id); };
  const close = () => {
    pendingSelection.current = null; setFocused(false); setLineage(false);
    requestAnimationFrame(() => {
      if (opener.current?.isConnected && opener.current.getClientRects().length) opener.current.focus();
      else document.getElementById("knowledge-search")?.focus();
    });
  };
  const unavailable = detailError || contextError || (!loading && !rows.some((row: KnowledgeRow) => row.id === selected));
  const related = relations.filter((edge: any) => (edge.from === selected || edge.to === selected) && rows.some((row: KnowledgeRow) => row.id === edge.from) && rows.some((row: KnowledgeRow) => row.id === edge.to));
  const selectedEvidence = current?.evidence?.[Number(graphSelection.split(":")[1])];
  return <div className={`knowledgeWorkspace${focused ? " hasRecord" : ""}`}>
    <section className="knowledgeLibrary" aria-label="Current knowledge">
      <header className="knowledgeHead"><div><h1>Knowledge</h1><p>Find what you can rely on, and the evidence behind it.</p></div><Button variant="outline" onClick={onReview}>Review{reviewCount ? ` (${reviewCount})` : ""}</Button></header>
      <div className="knowledgeSearch"><label htmlFor="knowledge-search">Search current claims</label><input id="knowledge-search" type="search" placeholder="Search statements, applicability, or keywords" value={query} onChange={event => setQuery(event.target.value)} /></div>
      <div className="knowledgeFilters"><label>Applicability<select aria-label="Applicability" value={topic} onChange={event => setTopic(event.target.value)}><option value="">All applicability</option>{topics.map(value => <option key={value}>{value}</option>)}</select></label><label>Sort by<select aria-label="Sort by" value={sort} onChange={event => setSort(event.target.value as KnowledgeSort)}><option value="newest">Newest proposed</option><option value="oldest">Oldest proposed</option><option value="statement">Statement A–Z</option></select></label></div>
      <div className="knowledgeCount" role="status"><strong>{loading ? "Loading knowledge…" : contextError ? "Knowledge unavailable" : `${visible.length}${query || topic ? ` of ${rows.length}` : ""} current ${visible.length === 1 ? "claim" : "claims"}`}</strong>{!loading && !contextError && <span>Eligible for this owner view</span>}</div>
      {lineage && <section className="knowledgeLineage"><Button variant="outline" onClick={() => setLineage(false)}>Back to claims</Button>{current && <><LineageGraph receipt={current} available evidenceNames={(current.evidence || []).map(evidenceName)} selection={graphSelection} onSelect={setGraphSelection} />{selectedEvidence && <section className="knowledgeGraphEvidence"><h2>{evidenceName(selectedEvidence)}</h2>{renderEvidence(selectedEvidence)}</section>}{graphSelection === "context" && <p>Included in the current owner context. Agent access remains credential-specific.</p>}<section className="relatedClaims"><h2>Related current claims</h2>{related.length ? related.map((edge: any, i: number) => { const other = rows.find((row: KnowledgeRow) => row.id === (edge.from === selected ? edge.to : edge.from)); return <button key={edge.id || i} onClick={() => focus(other.id)}><span>{edge.from === selected ? "Outgoing" : "Incoming"} · {String(edge.type).replaceAll("_", " ")} · {edge.state || "recorded"}</span><strong>{other.label}</strong></button>; }) : <p>No relations to other current claims recorded.</p>}</section></>}</section>}
      {!lineage && (loading ? <div className="knowledgeLoading" aria-busy="true">{[0, 1, 2].map(i => <div key={i}><span /><span /></div>)}</div> : contextError ? <div className="knowledgeEmpty"><h2>Current claims could not be loaded</h2><p>Use Reload workspace to try again.</p></div> : visible.length ? <ul className="knowledgeList">{visible.map(row => <li key={row.id}><button type="button" className={focused && selected === row.id ? "isSelected" : ""} aria-pressed={focused && selected === row.id} onClick={event => focus(row.id, event.currentTarget)}><span className="knowledgeListMeta">{knowledgeTopic(row) || "Applicability not recorded"}<span>{knowledgeDate(row.created_at)}</span></span><strong>{row.label}</strong>{row.applicability?.description && <span className="knowledgeDescription">{row.applicability.description}</span>}<span className="knowledgeRead">Read claim <ChevronRight /></span></button></li>)}</ul> : <div className="knowledgeEmpty"><h2>{rows.length ? "No matching claims" : "Your knowledge starts with a reviewed claim"}</h2><p>{rows.length ? "Try a broader search or a different applicability." : "Human-approved claims appear here when they are current and eligible for this owner view."}</p>{rows.length ? <Button variant="outline" onClick={() => { setQuery(""); setTopic(""); }}>Clear filters</Button> : <Button variant="outline" onClick={onReview}>Review candidate claims</Button>}</div>)}
    </section>
    {focused && (current ? <KnowledgeRecord key={current.claim.id} receipt={current} onClose={close} onLineage={() => { setLineage(true); setGraphSelection("claim"); setFocused(false); }} renderEvidence={renderEvidence} evidenceName={evidenceName} /> : <aside className="knowledgeRecord knowledgePending" aria-label="Knowledge record" aria-busy={!unavailable}><Button variant="outline" onClick={close}>Close record</Button><h2>{unavailable ? "Record unavailable" : "Loading claim record…"}</h2><p>{unavailable ? "This record is not available in the current owner context, or its receipt could not be loaded." : "Retrieving the statement, human decision, and bound evidence."}</p>{detailError && <Button variant="outline" onClick={() => onChoose(selected)}>Retry details</Button>}</aside>)}
  </div>;
}
