import React from "react";
import { Button } from "./ui/button";
import { claimDisplayTitle } from "./claim-display";
import { knowledgeTopic, type KnowledgeRow } from "./knowledge-model";
import "./claim-graph.css";

const RELATION_TYPES = new Set(["depends_on", "qualifies", "contradicts", "supersedes", "same_as", "re_proposed_as"]);
const CURRENT_RELATION_STATES = new Set(["admitted", "current"]);
const relationLabel = (value: string) => value.replaceAll("_", " ");
const relationState = (edge: any) => edge.state || "needs_review";

export function ClaimGraph({ rows, nodes, edges, relations, onChoose }: any) {
  const [selection, setSelection] = React.useState("");
  const claims = (rows as KnowledgeRow[]).slice(0, 10);
  const claimIds = new Set(claims.map(row => row.id));
  const support = edges.filter((edge: any) => edge.type === "supports" && claimIds.has(edge.to));
  const evidenceIds = [...new Set(support.map((edge: any) => edge.from))].slice(0, 16) as string[];
  const relationMap = new Map<string, any>();
  [...relations, ...edges.filter((edge: any) => RELATION_TYPES.has(edge.type))]
    .filter((edge: any) => claimIds.has(edge.from) && claimIds.has(edge.to))
    .forEach((edge: any) => {
      const key = edge.id || `${edge.from}:${edge.type}:${edge.to}`;
      const prior = relationMap.get(key) || {};
      relationMap.set(key, {...prior, ...edge, citation: edge.citation || edge.qualifiers?.citation || prior.citation});
    });
  const claimRelations = [...relationMap.values()].slice(0, 12);
  const contextGroups = [...new Set(claims.map(row => knowledgeTopic(row) || "Applicability not recorded"))];
  const height = Math.max(440, evidenceIds.length * 92 + 104, claims.length * 118 + 104, contextGroups.length * 118 + 104);
  const evidenceY = (index: number) => 78 + index * 92;
  const claimY = (index: number) => 78 + index * 118;
  const contextY = (index: number) => 78 + index * 118;
  const claimIndex = (id: string) => claims.findIndex(row => row.id === id);
  const groupIndex = (row: KnowledgeRow) => contextGroups.indexOf(knowledgeTopic(row) || "Applicability not recorded");
  const claimById = (id: string) => claims.find(row => row.id === id);
  const relationKey = (edge: any, index: number) => edge.id || `${edge.from}:${edge.type}:${edge.to}:${index}`;
  const selectedRelationIndex = selection.startsWith("relation:") ? Number(selection.split(":")[1]) : -1;
  const selectedRelation = claimRelations[selectedRelationIndex];
  const selectedClaim = selection.startsWith("claim:") ? claimById(selection.slice(6)) : null;
  const selectedEvidenceId = selection.startsWith("evidence:") ? selection.slice(9) : "";
  const selectedContext = selection.startsWith("context:") ? selection.slice(8) : "";
  const relatedToSelection = (id: string) => {
    if (!selection) return true;
    if (selectedEvidenceId) return support.some((edge: any) => edge.from === selectedEvidenceId && edge.to === id);
    if (selectedContext) return (knowledgeTopic(claimById(id)!) || "Applicability not recorded") === selectedContext;
    if (selectedRelation) return selectedRelation.from === id || selectedRelation.to === id;
    return selectedClaim?.id === id;
  };
  const select = (value: string) => setSelection(current => current === value ? "" : value);

  return <section className="claimMap" aria-label="Current claim graph">
    <header className="claimMapHead">
      <div>
        <h2>Current claim graph</h2>
        <p>Recorded evidence bindings, current admitted claims, and owner-view eligibility.</p>
        <p className="claimMapBoundary">This map explains recorded state. It does not approve claims or establish agent access; model advice remains advisory.</p>
      </div>
      <div className="claimMapLegend" aria-label="Graph legend"><span data-tone="evidence">Evidence</span><span data-tone="claim">Current admitted claim</span><span data-tone="context">Owner-view eligibility</span></div>
    </header>

    <div className="claimMapDesktop">
      <div className="claimMapScroll" tabIndex={0} aria-label="Scrollable claim graph canvas">
        <div className="claimMapPlane" style={{ "--claim-map-height": `${height}px` } as React.CSSProperties}>
          <div className="claimMapColumns"><span>Bound evidence</span><span>Current admitted claims</span><span>Owner-view eligibility</span></div>
          <svg viewBox={`0 0 1200 ${height}`} preserveAspectRatio="none" aria-hidden="true">
            <defs><marker id="claimRelationArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" /></marker></defs>
            {support.filter((edge: any) => evidenceIds.includes(edge.from)).map((edge: any, index: number) => {
              const from = evidenceIds.indexOf(edge.from), to = claimIndex(edge.to);
              return <path key={`support:${index}`} className="supportPath" d={`M 310 ${evidenceY(from) + 37} C 374 ${evidenceY(from) + 37}, 390 ${claimY(to) + 48}, 455 ${claimY(to) + 48}`} />;
            })}
            {claims.map((row, index) => <path key={`context:${row.id}`} className="contextPath" d={`M 785 ${claimY(index) + 48} C 834 ${claimY(index) + 48}, 850 ${contextY(groupIndex(row)) + 44}, 900 ${contextY(groupIndex(row)) + 44}`} />)}
            {claimRelations.map((edge: any, index: number) => {
              const from = claimIndex(edge.from), to = claimIndex(edge.to);
              const bend = 828 + (index % 3) * 20;
              const middle = (claimY(from) + claimY(to)) / 2 + 48;
              const state = relationState(edge);
              return <g key={relationKey(edge, index)} className={`relationPath relation-${edge.type} state-${state}${selectedRelationIndex === index ? " selected" : ""}`}>
                <path className="claimRelationLine" markerEnd="url(#claimRelationArrow)" d={`M 785 ${claimY(from) + 48} C ${bend} ${claimY(from) + 48}, ${bend} ${claimY(to) + 48}, 785 ${claimY(to) + 48}`} />
                <text x={bend + 5} y={middle - 5}>{relationLabel(edge.type)} · {relationLabel(state)}</text>
              </g>;
            })}
          </svg>
          {evidenceIds.map((id, index) => { const node = nodes.find((item: any) => item.id === id); const active = selection === `evidence:${id}`; return <Button key={id} variant="ghost" size="content" className="claimMapNode evidenceNode" style={{ top: evidenceY(index), opacity: selection && !active ? .42 : 1 }} aria-pressed={active} onClick={() => select(`evidence:${id}`)}><small>Evidence receipt</small><strong>{node?.label || "Bound evidence"}</strong><span>{support.filter((edge: any) => edge.from === id).length} supported {support.filter((edge: any) => edge.from === id).length === 1 ? "claim" : "claims"}</span></Button>; })}
          {claims.map((row, index) => { const active = selection === `claim:${row.id}`; return <Button key={row.id} variant="ghost" size="content" className="claimMapNode currentClaimNode" style={{ top: claimY(index), opacity: relatedToSelection(row.id) ? 1 : .28 }} aria-pressed={active} onClick={() => select(`claim:${row.id}`)}><small>Current admitted · {knowledgeTopic(row) || "Applicability not recorded"}</small><strong>{claimDisplayTitle(row)}</strong><span>{claimRelations.filter((edge: any) => edge.from === row.id || edge.to === row.id).length} recorded relations</span></Button>; })}
          {contextGroups.map((group, index) => { const count = claims.filter(row => (knowledgeTopic(row) || "Applicability not recorded") === group).length; const active = selection === `context:${group}`; return <Button key={group} variant="ghost" size="content" className="claimMapNode contextNode" style={{ top: contextY(index), opacity: selection && !active && !selection.startsWith("claim:") ? .42 : 1 }} aria-pressed={active} onClick={() => select(`context:${group}`)}><small>Eligible in this owner view</small><strong>{group}</strong><span>{count} current {count === 1 ? "claim" : "claims"} · agent access checked separately</span></Button>; })}
        </div>
      </div>
    </div>

    <div className="claimMapMobile" aria-label="Claim-centered lineage">
      {claims.map(row => {
        const incoming = claimRelations.filter((edge: any) => edge.to === row.id);
        const outgoing = claimRelations.filter((edge: any) => edge.from === row.id);
        const evidence = support.filter((edge: any) => edge.to === row.id).map((edge: any) => nodes.find((node: any) => node.id === edge.from));
        return <article className="claimLineageCard" key={row.id}>
          <div className="claimLineageHead"><small>Current admitted claim</small><strong>{claimDisplayTitle(row)}</strong><span>{knowledgeTopic(row) || "Applicability not recorded"}</span></div>
          <dl>
            <div><dt>Bound evidence</dt><dd>{evidence.length ? evidence.map((node: any) => <span key={node?.id}>{node?.label || "Evidence receipt"}</span>) : <span>None shown in this projection</span>}</dd></div>
            <div><dt>Recorded relations</dt><dd>{incoming.length + outgoing.length ? <>
              {incoming.map((edge: any, index: number) => <span key={`in:${relationKey(edge, index)}`}><b>{claimDisplayTitle(claimById(edge.from)!)}</b> → {relationLabel(edge.type)} → this claim <em data-state={relationState(edge)}>{relationLabel(relationState(edge))}</em>{edge.citation && <i>Citation bound</i>}{edge.advice?.recommendation && <i>Jev: {edge.advice.recommendation}</i>}</span>)}
              {outgoing.map((edge: any, index: number) => <span key={`out:${relationKey(edge, index)}`}>This claim → {relationLabel(edge.type)} → <b>{claimDisplayTitle(claimById(edge.to)!)}</b> <em data-state={relationState(edge)}>{relationLabel(relationState(edge))}</em>{edge.citation && <i>Citation bound</i>}{edge.advice?.recommendation && <i>Jev: {edge.advice.recommendation}</i>}</span>)}
            </> : <span>No claim-to-claim relations shown</span>}</dd></div>
            <div><dt>Owner-view eligibility</dt><dd><span>{knowledgeTopic(row) || "Applicability not recorded"} · agent access checked separately</span></dd></div>
          </dl>
          <Button variant="outline" size="sm" onClick={event => onChoose(row.id, event.currentTarget)}>Open claim record</Button>
        </article>;
      })}
    </div>

    <div className="claimRelationControls" aria-label="Recorded claim relations">
      <div className="claimRelationControlsHead"><strong>Recorded claim relations</strong><span>Direction and lifecycle state are explicit.</span></div>
      {claimRelations.length ? <div className="claimRelationList">{claimRelations.map((edge: any, index: number) => {
        const active = selectedRelationIndex === index;
        const state = relationState(edge);
        return <Button key={relationKey(edge, index)} variant="ghost" size="content" className="claimRelationButton" aria-pressed={active} onClick={() => select(`relation:${index}`)}>
          <span className="relationStatement"><b>{claimDisplayTitle(claimById(edge.from)!)}</b><span aria-hidden="true">→</span><span>{relationLabel(edge.type)}</span><span aria-hidden="true">→</span><b>{claimDisplayTitle(claimById(edge.to)!)}</b></span>
          <span className="relationSignals">{edge.citation && <i>Citation bound</i>}{edge.advice?.recommendation && <i>Jev: {edge.advice.recommendation}</i>}<em data-state={state}>{CURRENT_RELATION_STATES.has(state) ? "Current admitted" : relationLabel(state)}</em></span>
        </Button>;
      })}</div> : <p className="claimRelationEmpty">No claim-to-claim relations recorded in this projection.</p>}
    </div>

    {selection && <aside className="claimMapInspector" aria-live="polite">
      <div>
        <small>{selectedRelation ? "Recorded relation" : selectedClaim ? "Current admitted claim" : selectedEvidenceId ? "Evidence receipt" : "Owner-view eligibility"}</small>
        <strong>{selectedRelation ? `${claimDisplayTitle(claimById(selectedRelation.from)!)} → ${relationLabel(selectedRelation.type)} → ${claimDisplayTitle(claimById(selectedRelation.to)!)}` : selectedClaim ? claimDisplayTitle(selectedClaim) : selectedEvidenceId ? nodes.find((node: any) => node.id === selectedEvidenceId)?.label || "Bound evidence" : selectedContext}</strong>
        <span>{selectedRelation ? `Lifecycle state: ${relationLabel(relationState(selectedRelation))}.${selectedRelation.citation ? ` Citation bound to evidence ${selectedRelation.citation.evidence_ref}.` : " No relation citation recorded."}${selectedRelation.advice?.recommendation ? ` Jev advice: ${selectedRelation.advice.recommendation}; advisory only.` : ""} A recorded edge or model recommendation does not itself approve either claim.` : selectedClaim ? "Current in this owner view. Agent access is evaluated separately." : selectedEvidenceId ? "This receipt is recorded as evidence; the binding does not by itself admit the claim." : "This grouping describes owner-view eligibility, not universal or credential-independent access."}</span>
      </div>
      <div className="claimMapInspectorActions">{selectedClaim && <Button variant="outline" size="sm" onClick={event => onChoose(selectedClaim.id, event.currentTarget)}>Open claim record</Button>}<Button variant="ghost" size="sm" onClick={() => setSelection("")}>Clear selection</Button></div>
    </aside>}

    <footer className="claimMapFooter">
      <span>Showing the first {claims.length} of {rows.length} current claims in this projection</span>
      <span>{claimRelations.length ? `${claimRelations.length} recorded claim relations shown` : "No claim-to-claim relations recorded in this projection"}</span>
    </footer>
  </section>;
}
