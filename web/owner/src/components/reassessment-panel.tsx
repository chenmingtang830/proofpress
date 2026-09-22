import React from "react";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Checkbox } from "./ui/checkbox";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";

export type DependencyImpact = {
  reason: string;
  upstream_id: string;
  relation_id?: string | null;
  path: string[];
};

export type DependencyRelation = {
  id: string;
  upstream?: { id: string; title?: string | null; statement?: string | null };
};

type ReassessmentPanelProps = {
  claimId: string;
  impacts: DependencyImpact[];
  dependencies: DependencyRelation[];
  redacted: number;
  note: string;
  setNote: (note: string) => void;
  busy: boolean;
  showDecision: boolean;
  onReassess: (decision: "retain" | "request_changes", relationIds: string[]) => void;
};

const reasonLabels: Record<string, string> = {
  withdrawn: "Required claim withdrawn",
  superseded: "Required claim superseded",
  expired: "Required claim expired",
  missing: "Required claim unavailable",
  dependency_changed: "Dependency authority changed",
  relation_rejected: "Dependency approval rejected",
  relation_needs_revision: "Dependency needs revision",
  relation_unresolved: "Dependency approval is stale",
};

export function ReassessmentPanel({ claimId, impacts, dependencies, redacted, note, setNote, busy, showDecision, onReassess }: ReassessmentPanelProps) {
  const [retired, setRetired] = React.useState<string[]>([]);
  React.useEffect(() => setRetired([]), [claimId]);
  const transitiveBlocked = impacts.some(item => item.path.length > 2);
  const directInvalid = impacts.filter(item => item.path.length === 2 && item.relation_id && item.reason !== "dependency_changed");
  const retainBlocked = busy || !note.trim() || transitiveBlocked || directInvalid.some(item => !retired.includes(item.relation_id!));

  return <>
    <section className="reassessmentPanel" aria-label="Dependency reassessment">
      <Badge state="dependency_invalidated" /><h3>Reuse is paused</h3>
      <p>The previous approval remains on record. Review the changed dependency path and record a fresh Owner decision.</p>
      <fieldset className="dependencyChoices"><legend>Dependencies requiring resolution</legend>{impacts.map((item, index) => {
        const relation = dependencies.find(candidate => candidate.id === item.relation_id);
        const relationLabel = relation?.upstream?.title || relation?.upstream?.statement || "Required upstream claim";
        const describedBy = `dependency-${item.relation_id || index}-details`;
        return <div className="dependencyReason" key={item.relation_id || index}>
          <strong>{reasonLabels[item.reason] || item.reason.replaceAll("_", " ")}</strong>
          <span>{relationLabel} · {item.path.length === 2 ? "Direct" : "Transitive"} impact</span>
          <small id={describedBy} className="mono">{item.path.join(" → ")}{item.relation_id ? ` · ${item.relation_id}` : ""}</small>
          {item.path.length === 2 && item.relation_id && <Label><Checkbox aria-describedby={describedBy} checked={retired.includes(item.relation_id)} onCheckedChange={checked => setRetired(current => checked ? [...new Set([...current, item.relation_id!])] : current.filter(id => id !== item.relation_id))} /> Retire dependency on {relationLabel}</Label>}
        </div>;
      })}</fieldset>
      {redacted > 0 && <p>{redacted} upstream {redacted === 1 ? "detail is" : "details are"} hidden by the current visibility policy.</p>}
    </section>
    {showDecision && <Card className="decision reassessmentDecision">
      <div className="decisionHeading"><span>Owner reassessment</span><p>Retain only after every invalid dependency is retired or otherwise resolved. Proofpress does not judge whether independent evidence is sufficient.</p></div>
      <Label htmlFor={`reassessment-note-${claimId}`}>Reassessment reason <small>Required</small></Label>
      <Textarea id={`reassessment-note-${claimId}`} value={note} onChange={event => setNote(event.target.value)} placeholder="Explain the independent support or the bounded revision required." />
      <ul className="reassessmentChecklist"><li>{note.trim() ? "Reason recorded" : "Add a reassessment reason"}</li><li>{retired.length ? `${retired.length} direct relation selected` : "Select each invalid direct dependency to retire"}</li><li>{transitiveBlocked ? "Transitive blocker must be resolved upstream" : "No transitive blockers"}</li></ul>
      <div><Button className="reassessmentRequest" variant="request" disabled={busy || !note.trim()} onClick={() => onReassess("request_changes", [])}>Request revision</Button><Button className="reassessmentRetain" variant={retainBlocked ? "outline" : "approve"} disabled={retainBlocked} onClick={() => onReassess("retain", retired)}>Retain with independent support</Button></div>
      {transitiveBlocked && <small>Resolve the invalidated upstream claim first; this claim has a transitive dependency path that cannot be retired here.</small>}
    </Card>}
  </>;
}
