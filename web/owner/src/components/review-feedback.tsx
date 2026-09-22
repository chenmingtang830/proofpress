import { Alert } from "./ui/alert";
import { Textarea } from "@/components/ui/textarea";
import React from "react";
import { Check, X } from "./ui/icon";
import { Button } from "./ui/button";

export function revisionInstructions(r: any) {
  if (!r?.revision_request) return "";
  return `Read proofpress_get_review_receipt for ${r.claim.id}. Requested change: ${r.review?.note || ""}\nSubmit supporting evidence, then use proofpress_propose_claim with qualifiers: ${JSON.stringify({revision_of:r.claim.id,revision_request_ref:r.revision_request.event_id})}. Preserve other required profile qualifiers and state the revised applicability. Run evaluation, then return the new review link. Do not approve or overwrite the original.`;
}

export function DecisionNotice({state, children}: any) {
  const title = state === "needs_revision" ? "Changes requested" : state === "admitted" ? "Approved for reuse" : state === "rejected" ? "Rejected" : "Not available for reuse";
  const excluded = ["blocked", "rejected", "withdrawn", "dependency_invalidated"].includes(state);
  return <Alert className="decisionNotice" data-state={state} role="status">{excluded ? <X aria-hidden="true" /> : <Check aria-hidden="true" />}<div><strong>{title}</strong>{children}</div></Alert>;
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
  React.useEffect(() => { setStatus("idle"); }, [receipt.claim.id]);
  if (!text) return <p>Revision receipt unavailable. Refresh this page to retry.</p>;
  return <div className="handoffInstructions">
    {autoCopy && <p className={status === "copied" ? "copySuccess" : ""} role="status">{status === "copied" && <Check />}{status === "copied" ? "Copied to clipboard. Paste into your agent." : status === "failed" ? "Your browser blocked automatic copying." : "Copying instructions…"}</p>}
    {status === "failed" && <Textarea ref={field} readOnly aria-label="Revision instructions" value={text} />}
    {!autoCopy && status === "copied" ? <span className="copySuccess" role="status"><Check />Copied to clipboard</span> : (!autoCopy || status === "failed") && <Button variant="outline" disabled={status === "copying"} onClick={() => void copy()}>{status === "copying" ? "Copying…" : "Copy instructions for agent"}</Button>}
    {status === "failed" && <Button variant="outline" onClick={() => { field.current?.focus(); field.current?.select(); }}>Select instructions</Button>}
  </div>;
}

export function BlockedCorrectionHandoff({receipt}: any) {
  const [status, setStatus] = React.useState<"idle"|"copied"|"failed">("idle");
  const field = React.useRef<HTMLTextAreaElement>(null);
  const failed = Object.entries(receipt?.evaluation?.checks || {}).filter(([, passed]) => !passed).map(([name]) => name.replaceAll("_", " "));
  const instructions = `Review Proofpress candidate ${receipt?.claim?.id || ""}. Deterministic checks failed: ${failed.join(", ") || "see the current review receipt"}. Correct the evidence or claim and submit a new candidate for owner review. Keep the blocked candidate excluded from reuse; do not overwrite or approve it.`;
  async function copy() {
    try { await navigator.clipboard.writeText(instructions); setStatus("copied"); }
    catch { setStatus("failed"); }
  }
  return <section className="blockedCorrectionHandoff" aria-label="Correction handoff">
    <div><strong>Next step</strong><p>Ask {receipt?.claim?.proposer || "the proposing agent"} to address these checks and submit a corrected candidate. This blocked claim stays excluded from reuse.</p></div>
    {failed.length > 0 && <ul aria-label="Failed deterministic checks">{failed.map((name:string) => <li key={name}>{name}</li>)}</ul>}
    <Button variant="outline" onClick={() => void copy()}>{status === "copied" ? "Instructions copied" : "Copy instructions for proposer"}</Button>
    {status === "failed" && <><p role="status">Clipboard access failed. Select and copy these instructions.</p><Textarea ref={field} readOnly aria-label="Correction instructions" value={instructions} /><Button variant="ghost" onClick={() => { field.current?.focus(); field.current?.select(); }}>Select instructions</Button></>}
    {status === "copied" && <span className="copySuccess" role="status">Instructions copied. Share them with the proposer.</span>}
  </section>;
}

export function RevisionPanel({receipt, onChoose}: any) {
  return <section className="revisionPanel"><h3>Requested change</h3><blockquote>{receipt.review?.note || "No note recorded."}</blockquote><RevisionInstructions key={receipt.revision_request.event_id} receipt={receipt} />{receipt.revisions?.length > 0 && <div className="revisionSubmissions"><h4>Revised proposals</h4>{receipt.revisions.map((candidate:any) => <Button key={candidate.id} variant="outline" onClick={() => onChoose(candidate.id)}>{candidate.statement.slice(0,120)} · {candidate.state}</Button>)}</div>}</section>;
}

export function historyActor(event: any): string {
  const actor = event.reviewer || event.claim?.proposer || event.verifier || event.judge || event.actor;
  const identity = typeof actor === "string" ? actor : actor?.id || actor?.name;
  return [identity || "Actor not recorded", event.model].filter(Boolean).join(" · ");
}
