import React from "react";
import { Check } from "./ui/icon";
import { Button } from "./ui/button";

export function revisionInstructions(r: any) {
  if (!r?.revision_request) return "";
  return `Read proofpress_get_review_receipt for ${r.conclusion.id}. Requested change: ${r.review?.note || ""}\nSubmit supporting evidence, then use proofpress_propose_conclusion with the same scope and qualifiers: ${JSON.stringify({revision_of:r.conclusion.id,revision_request_ref:r.revision_request.event_id})}. Preserve other required profile qualifiers. Run evaluation, then return the new review link. Do not approve or overwrite the original.`;
}

export function DecisionNotice({state, children}: any) {
  const title = state === "needs_revision" ? "Changes requested" : state === "admitted" ? "Approved for reuse" : state === "rejected" ? "Rejected" : "Not available for reuse";
  return <div className="decisionNotice" data-state={state} role="status"><Check aria-hidden="true" /><div><strong>{title}</strong>{children}</div></div>;
}

export function RevisionInstructions({receipt, autoCopy = false}: any) {
  const [status, setStatus] = React.useState<"idle"|"copying"|"copied"|"failed">("idle");
  const field = React.useRef<HTMLTextAreaElement>(null);
  const text = revisionInstructions(receipt);
  const copy = React.useCallback(async () => {
    setStatus("copying");
    try { await navigator.clipboard.writeText(text); setStatus("copied"); }
    catch { setStatus("failed"); }
  }, [text]);
  React.useEffect(() => { if (autoCopy && text) void copy(); }, [autoCopy, text, copy]);
  React.useEffect(() => { setStatus("idle"); }, [receipt.conclusion.id]);
  if (!text) return <p>Revision receipt unavailable. Refresh this page to retry.</p>;
  return <div className="handoffInstructions">
    {autoCopy && <p role="status">{status === "copied" ? "Copied to clipboard. Paste into your agent." : status === "failed" ? "Your browser blocked automatic copying." : "Copying instructions…"}</p>}
    {status === "failed" && <textarea ref={field} readOnly aria-label="Revision instructions" value={text} />}
    {(!autoCopy || status === "failed") && <Button variant="outline" onClick={() => void copy()}>{status === "copied" ? "Copied" : "Copy instructions for agent"}</Button>}
    {status === "failed" && <Button variant="outline" onClick={() => { field.current?.focus(); field.current?.select(); }}>Select instructions</Button>}
  </div>;
}

export function RevisionPanel({receipt, onChoose}: any) {
  return <section className="revisionPanel"><h3>Requested change</h3><blockquote>{receipt.review?.note || "No note recorded."}</blockquote><RevisionInstructions key={receipt.revision_request.event_id} receipt={receipt} />{receipt.revisions?.length > 0 && <div className="revisionSubmissions"><h4>Revised proposals</h4>{receipt.revisions.map((candidate:any) => <Button key={candidate.id} variant="outline" onClick={() => onChoose(candidate.id)}>{candidate.statement.slice(0,120)} · {candidate.state}</Button>)}</div>}</section>;
}

export function historyActor(event: any): string {
  const actor = event.reviewer || event.conclusion?.proposer || event.verifier || event.judge || event.actor;
  const identity = typeof actor === "string" ? actor : actor?.id || actor?.name;
  return [identity || "Actor not recorded", event.model].filter(Boolean).join(" · ");
}
