import React from "react";
import { Button } from "./ui/button";
import { claimDisplayTitle, claimStatement } from "./claim-display";
import { knowledgeTopic, type KnowledgeRow } from "./knowledge-model";
import "./claim-graph.css";

const RELATION_TYPES = new Set(["supports", "depends_on", "qualifies", "contradicts", "supersedes", "same_as", "re_proposed_as"]);
const CURRENT_RELATION_STATES = new Set(["admitted", "current"]);
const relationLabel = (value: string) => value.replaceAll("_", " ");
const relationState = (edge: any) => edge.state || "needs_review";
const relationAdviceAttribution = (advice: any) => [advice?.adapter, advice?.model].filter(Boolean).join(" · ") || "Model";

export type GraphInspection = {
  key: string;
  kind: "claim" | "evidence" | "relation";
  title: string;
  claimId?: string;
  statement?: string;
  scope?: string;
  count?: number;
  from?: string;
  to?: string;
  state?: string;
  evidenceRef?: string;
  advice?: string;
};

export function ClaimGraph({ rows, nodes, edges, relations, onChoose, inspection, onInspect }: any) {
  const selection = (inspection as GraphInspection | null)?.key || "";
  const [claimLimit, setClaimLimit] = React.useState(6);
  const [evidenceLimit, setEvidenceLimit] = React.useState(16);
  const [relationsOpen, setRelationsOpen] = React.useState(false);
  const allClaims = rows as KnowledgeRow[];
  const claims = allClaims.slice(0, claimLimit);
  const claimIds = new Set(claims.map(row => row.id));
  const nodeTypes = new Map(nodes.map((node: any) => [node.id, node.type]));
  const isClaimNode = (id: string) => claimIds.has(id) || nodeTypes.get(id) === "claim";
  const support = edges.filter((edge: any) => edge.type === "supports" && claimIds.has(edge.to) && !isClaimNode(edge.from));
  const allEvidenceIds = [...new Set(support.map((edge: any) => edge.from))] as string[];
  const evidenceIds = allEvidenceIds.slice(0, evidenceLimit);
  const evidenceLabel = (id: string) => {
    const sourceId = edges.find((edge: any) => edge.type === "bound_as" && edge.to === id)?.from;
    return nodes.find((node: any) => node.id === sourceId)?.label || nodes.find((node: any) => node.id === id)?.label || "Bound evidence";
  };
  const relationMap = new Map<string, any>();
  [...relations, ...edges.filter((edge: any) => RELATION_TYPES.has(edge.type))]
    .filter((edge: any) => claimIds.has(edge.from) && claimIds.has(edge.to))
    .forEach((edge: any) => {
      const key = edge.id || `${edge.from}:${edge.type}:${edge.to}`;
      const prior = relationMap.get(key) || {};
      relationMap.set(key, {...prior, ...edge, citation: edge.citation || edge.qualifiers?.citation || prior.citation});
    });
  const claimRelations = [...relationMap.values()];
  const evidenceStep = 100;
  const claimStep = 132;
  const evidenceAnchor = 43;
  const claimAnchor = 56;
  const height = Math.max(460, evidenceIds.length * evidenceStep + 112, claims.length * claimStep + 112);
  const evidenceY = (index: number) => 78 + index * evidenceStep;
  const claimY = (index: number) => 78 + index * claimStep;
  const claimIndex = (id: string) => claims.findIndex(row => row.id === id);
  const claimById = (id: string) => claims.find(row => row.id === id);
  const relationKey = (edge: any) => edge.id || `${edge.from}:${edge.type}:${edge.to}`;
  const selectedRelationKey = selection.startsWith("relation:") ? selection.slice(9) : "";
  const selectedRelationIndex = claimRelations.findIndex((edge: any) => relationKey(edge) === selectedRelationKey);
  const selectedRelation = selectedRelationIndex >= 0 ? claimRelations[selectedRelationIndex] : null;
  const selectedClaim = selection.startsWith("claim:") ? claimById(selection.slice(6)) : null;
  const selectedEvidenceId = selection.startsWith("evidence:") ? selection.slice(9) : "";
  React.useEffect(() => {
    const valid = !selection
      || selection.startsWith("relation:") && Boolean(selectedRelation)
      || selection.startsWith("claim:") && Boolean(selectedClaim)
      || selection.startsWith("evidence:") && evidenceIds.includes(selectedEvidenceId);
    if (!valid) onInspect(null);
  }, [selection, selectedRelation, selectedClaim, selectedEvidenceId, evidenceIds, onInspect]);
  const visibleRelations = selectedRelation
    ? [selectedRelation]
    : selectedClaim
      ? claimRelations.filter((edge: any) => edge.from === selectedClaim.id || edge.to === selectedClaim.id)
      : [];
  const evidenceRelatedToSelection = (id: string) => {
    if (!selection) return true;
    if (selectedEvidenceId) return selectedEvidenceId === id;
    const targetIds = selectedRelation ? [selectedRelation.from, selectedRelation.to] : selectedClaim ? [selectedClaim.id] : [];
    return support.some((edge: any) => edge.from === id && targetIds.includes(edge.to));
  };
  const relatedToSelection = (id: string) => {
    if (!selection) return true;
    if (selectedEvidenceId) return support.some((edge: any) => edge.from === selectedEvidenceId && edge.to === id);
    if (selectedRelation) return selectedRelation.from === id || selectedRelation.to === id;
    return selectedClaim?.id === id;
  };
  const select = (value: string, element: HTMLElement) => {
    if (selection === value) { onInspect(null); return; }
    if (value.startsWith("claim:")) {
      const row = claimById(value.slice(6));
      if (row) onInspect({ key: value, kind: "claim", title: claimDisplayTitle(row), claimId: row.id, statement: claimStatement(row), scope: knowledgeTopic(row) || "Not recorded", count: claimRelations.filter((edge: any) => edge.from === row.id || edge.to === row.id).length } satisfies GraphInspection, element);
    } else if (value.startsWith("evidence:")) {
      const id = value.slice(9);
      onInspect({ key: value, kind: "evidence", title: evidenceLabel(id), evidenceRef: id, count: support.filter((edge: any) => edge.from === id).length } satisfies GraphInspection, element);
    } else {
      const edge = claimRelations.find((item: any) => relationKey(item) === value.slice(9));
      if (edge) onInspect({ key: value, kind: "relation", title: relationLabel(edge.type), from: claimDisplayTitle(claimById(edge.from)!), to: claimDisplayTitle(claimById(edge.to)!), state: relationLabel(relationState(edge)), evidenceRef: edge.citation?.evidence_ref, advice: edge.advice?.recommendation ? `${relationAdviceAttribution(edge.advice)} · ${edge.advice.recommendation} · advisory` : undefined } satisfies GraphInspection, element);
    }
  };

  return <section className="claimMap" aria-label="Current claim graph">
    <header className="claimMapHead">
      <div>
        <h2>Current claim graph</h2>
        <p className="claimMapBoundary">Recorded state only; model advice remains advisory. Approval and access are separate.</p>
      </div>
    </header>

    <div className="claimMapWorkspace" style={{ "--claim-map-height": `${height}px` } as React.CSSProperties}>
      <div className="claimMapPrimary">
      <div className="claimMapDesktop">
      <div className="claimMapScroll" tabIndex={0} aria-label="Scrollable claim graph canvas">
        <div className="claimMapPlane" style={{ "--claim-map-height": `${height}px` } as React.CSSProperties}>
          <div className="claimMapColumns"><span>Bound evidence</span><span>Current admitted claims</span></div>
          <svg viewBox={`0 0 900 ${height}`} preserveAspectRatio="none" aria-hidden="true">
            <defs><marker id="claimRelationArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" /></marker></defs>
            {support.filter((edge: any) => evidenceIds.includes(edge.from)).map((edge: any, index: number) => {
              const from = evidenceIds.indexOf(edge.from), to = claimIndex(edge.to);
              const active = !selection || evidenceRelatedToSelection(edge.from) && relatedToSelection(edge.to);
              return <path key={`support:${index}`} className="supportPath" style={{ opacity: active ? 1 : .12 }} d={`M 310 ${evidenceY(from) + evidenceAnchor} C 380 ${evidenceY(from) + evidenceAnchor}, 410 ${claimY(to) + claimAnchor}, 480 ${claimY(to) + claimAnchor}`} />;
            })}
            {visibleRelations.map((edge: any) => {
              const index = claimRelations.indexOf(edge);
              const from = claimIndex(edge.from), to = claimIndex(edge.to);
              const start = selection ? 864 : 810;
              const bend = selection ? 880 + (index % 2) * 10 : 840 + (index % 3) * 18;
              const middle = (claimY(from) + claimY(to)) / 2 + claimAnchor;
              const state = relationState(edge);
              return <g key={relationKey(edge)} className={`relationPath relation-${edge.type} state-${state}${selectedRelationIndex === index ? " selected" : ""}`}>
                <path className="claimRelationLine" markerEnd="url(#claimRelationArrow)" d={`M ${start} ${claimY(from) + claimAnchor} C ${bend} ${claimY(from) + claimAnchor}, ${bend} ${claimY(to) + claimAnchor}, ${start} ${claimY(to) + claimAnchor}`} />
                <text x="892" y={middle - 7} textAnchor="end">{relationLabel(edge.type)} · {relationLabel(state)}</text>
              </g>;
            })}
          </svg>
          {evidenceIds.map((id, index) => { const active = selection === `evidence:${id}`; const count = support.filter((edge: any) => edge.from === id).length; return <Button key={id} variant="ghost" size="content" className="claimMapNode evidenceNode" style={{ top: evidenceY(index), opacity: evidenceRelatedToSelection(id) ? 1 : .28 }} aria-pressed={active} onClick={event => select(`evidence:${id}`, event.currentTarget)}><small>Evidence</small><strong>{evidenceLabel(id)}</strong><span>{count} {count === 1 ? "claim" : "claims"}</span></Button>; })}
          {claims.map((row, index) => { const active = selection === `claim:${row.id}`; const count = claimRelations.filter((edge: any) => edge.from === row.id || edge.to === row.id).length; return <Button key={row.id} variant="ghost" size="content" className="claimMapNode currentClaimNode" style={{ top: claimY(index), opacity: relatedToSelection(row.id) ? 1 : .28 }} aria-pressed={active} onClick={event => select(`claim:${row.id}`, event.currentTarget)}><small>{knowledgeTopic(row) || "Scope not recorded"}</small><strong>{claimDisplayTitle(row)}</strong><span>{count} {count === 1 ? "relation" : "relations"}</span></Button>; })}
        </div>
      </div>
      </div>

      <div className="claimMapMobile" aria-label="Claim-centered lineage">
      {claims.map(row => {
        const incoming = claimRelations.filter((edge: any) => edge.to === row.id);
        const outgoing = claimRelations.filter((edge: any) => edge.from === row.id);
        const evidence = support.filter((edge: any) => edge.to === row.id && evidenceIds.includes(edge.from)).map((edge: any) => ({id:edge.from,label:evidenceLabel(edge.from)}));
        return <article className="claimLineageCard" key={row.id}>
          <div className="claimLineageHead"><strong>{claimDisplayTitle(row)}</strong><span>{knowledgeTopic(row) || "Scope not recorded"}</span></div>
          <dl>
            <div><dt>Bound evidence</dt><dd>{evidence.length ? evidence.map((node: any) => <span key={node?.id}>{node?.label || "Evidence receipt"}</span>) : <span>None shown in this projection</span>}</dd></div>
            <div><dt>Recorded relations</dt><dd>{incoming.length + outgoing.length ? <>
              {incoming.map((edge: any) => <span key={`in:${relationKey(edge)}`}><b>{claimDisplayTitle(claimById(edge.from)!)}</b> → {relationLabel(edge.type)} → this claim <em data-state={relationState(edge)}>{relationLabel(relationState(edge))}</em>{edge.citation && <i>Citation bound</i>}{edge.advice?.recommendation && <i>{relationAdviceAttribution(edge.advice)}: {edge.advice.recommendation}</i>}</span>)}
              {outgoing.map((edge: any) => <span key={`out:${relationKey(edge)}`}>This claim → {relationLabel(edge.type)} → <b>{claimDisplayTitle(claimById(edge.to)!)}</b> <em data-state={relationState(edge)}>{relationLabel(relationState(edge))}</em>{edge.citation && <i>Citation bound</i>}{edge.advice?.recommendation && <i>{relationAdviceAttribution(edge.advice)}: {edge.advice.recommendation}</i>}</span>)}
            </> : <span>No claim-to-claim relations shown</span>}</dd></div>
          </dl>
          <Button variant="outline" size="sm" onClick={event => onChoose(row.id, event.currentTarget)}>Open claim record</Button>
        </article>;
      })}
      </div>

      <div className="claimRelationControls" aria-label="Recorded claim relations">
      <div className="claimRelationControlsHead"><strong>{claimRelations.length} {claimRelations.length === 1 ? "relation" : "relations"}</strong>{claimRelations.length > 0 && <Button variant="ghost" size="sm" aria-expanded={relationsOpen} onClick={() => setRelationsOpen(open => !open)}>{relationsOpen ? "Hide" : "Show"}</Button>}</div>
      {relationsOpen && (claimRelations.length ? <div className="claimRelationList">{claimRelations.map((edge: any, index: number) => {
        const active = selectedRelationIndex === index;
        const state = relationState(edge);
        return <Button key={relationKey(edge)} variant="ghost" size="content" className="claimRelationButton" aria-pressed={active} onClick={event => select(`relation:${relationKey(edge)}`, event.currentTarget)}>
          <span className="relationStatement"><b>{claimDisplayTitle(claimById(edge.from)!)}</b><span aria-hidden="true">→</span><span>{relationLabel(edge.type)}</span><span aria-hidden="true">→</span><b>{claimDisplayTitle(claimById(edge.to)!)}</b></span>
          <span className="relationSignals">{edge.citation && <i>Citation bound</i>}{edge.advice?.recommendation && <i>{relationAdviceAttribution(edge.advice)}: {edge.advice.recommendation}</i>}<em data-state={state}>{CURRENT_RELATION_STATES.has(state) ? "Current admitted" : relationLabel(state)}</em></span>
        </Button>;
      })}</div> : <p className="claimRelationEmpty">No claim-to-claim relations recorded in this projection.</p>)}
      </div>
      </div>

    </div>

    {(allClaims.length > claims.length || allEvidenceIds.length > evidenceIds.length) && <footer className="claimMapFooter">
      <div>{allClaims.length > claims.length && <span>Showing {claims.length} of {allClaims.length} claims</span>}{allEvidenceIds.length > evidenceIds.length && <span>Showing {evidenceIds.length} of {allEvidenceIds.length} evidence receipts</span>}</div>
      <div>{allClaims.length > claims.length && <Button variant="outline" size="sm" onClick={() => setClaimLimit(limit => Math.min(limit + 6, allClaims.length))}>Show {Math.min(6, allClaims.length - claims.length)} more claims</Button>}{allEvidenceIds.length > evidenceIds.length && <Button variant="outline" size="sm" onClick={() => setEvidenceLimit(limit => Math.min(limit + 16, allEvidenceIds.length))}>Show {Math.min(16, allEvidenceIds.length - evidenceIds.length)} more evidence</Button>}</div>
    </footer>}
  </section>;
}
