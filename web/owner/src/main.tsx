import React from "react";
import { createRoot } from "react-dom/client";
import * as Tabs from "@radix-ui/react-tabs";
import * as Dialog from "@radix-ui/react-dialog";
import {
  Activity,
  BookOpen,
  Check,
  ChevronRight,
  Home,
  KeyRound,
  ShieldCheck,
  X,
} from "@/components/ui/icon";
import { Badge } from "@/components/ui/badge";
import { ActivityResult } from "@/components/activity-result";
import { ReviewPolicy } from "@/components/review-policy";
import { Button } from "@/components/ui/button";
import { DecisionNotice, RevisionInstructions, RevisionPanel, historyActor } from "@/components/review-feedback";
import { LineageGraph } from "@/components/lineage-graph";
import { LedgerOverview } from "@/components/ledger-overview";
import { ModalSurface } from "@/components/ui/modal-surface";
import "./index.css";
import "./components/governance.css";

type NodeRow = {
  id: string;
  type: string;
  label: string;
  state: string;
  scope?: string;
  created_at?: string;
};
type Receipt = {
  state: string;
  conclusion: {
    id: string;
    statement: string;
    scope?: string;
    proposer?: string;
    created_at?: string;
  };
  evidence?: any[];
  evaluation?: { checks?: Record<string, boolean> };
  recommendation?: { recommendation?: string; rationale?: string };
  history?: any[];
  judge_job?: {state:string;detail:string};
  review_policy?: {require_judge:boolean;mode:string;model:string;rubric:string;checks_current:boolean;advice_current:boolean};
};
type Page = "home" | "review" | "ledger" | "activity" | "admin";
const labels: Record<Page, string> = {
  home: "Home",
  review: "Review",
  ledger: "Ledger",
  activity: "Activity",
  admin: "Admin",
};
const icons = {
  home: Home,
  review: ShieldCheck,
  ledger: BookOpen,
  activity: Activity,
  admin: KeyRound,
};

async function api(path: string, options: RequestInit = {}) {
  const response = await fetch(path, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (response.status === 401) throw new Error("Your owner session has expired. Sign in again to continue.");
  let body: any;
  try { body = await response.json(); }
  catch { throw new Error(`The service returned an unreadable response (${response.status}). Reload the workspace to retry.`); }
  if (!response.ok || body.ok === false)
    throw new Error(
      body.error?.message ||
        body.error ||
        `Request failed (${response.status})`,
    );
  return body.result ?? body;
}
function evidenceName(row: any) {
  const p = row?.experiment_profile || {};
  if (p.cell) return p.cell.table?.identity || "Table cell";
  if (p.observation) return p.observation.metric?.name || "Metric observation";
  if (p.derivation) return p.derivation.formula?.name || "Derivation";
  return row?.retrieval_receipt?.source?.uri || row?.source?.uri || row?.path || row?.kind || "Evidence reference";
}
function evidenceText(row: any) {
  const p = row?.experiment_profile || {};
  if (p.cell) return `${p.cell.value} ${p.cell.unit || ""}`;
  if (p.observation)
    return `${p.observation.value} ${p.observation.unit || ""}`;
  if (p.derivation)
    return `${p.derivation.formula?.operation || "recompute"} → ${p.derivation.output?.value}`;
  return row?.retrieval_receipt?.quote || row?.quote || "No quote available in this receipt.";
}

function EvidenceContent({ row }: { row: any }) {
  const text = evidenceText(row);
  let structured: any = null;
  if (typeof text === "string") {
    try { structured = JSON.parse(text); } catch { /* A source quote is usually plain text. */ }
  }
  const renderValue = (value: any): React.ReactNode => {
    if (value === null) return "Not provided";
    if (typeof value !== "object") return String(value);
    if (Array.isArray(value)) return <ul>{value.map((item, i) => <li key={i}>{renderValue(item)}</li>)}</ul>;
    return <dl className="evidenceFields">{Object.entries(value).map(([key, value]) => <div key={key}><dt>{key.replaceAll("_", " ")}</dt><dd>{renderValue(value)}</dd></div>)}</dl>;
  };
  return <>{structured !== null ? renderValue(structured) : <p>{text}</p>}
    <details className="technicalDetails"><summary>Technical receipt</summary><pre>{JSON.stringify(row, null, 2)}</pre></details>
  </>;
}

function App() {
  const path = (location.pathname.split("/")[1] || "review") as Page;
  const [page, setPage] = React.useState<Page>(labels[path] ? path : "review");
  const [fullReview, setFullReview] = React.useState(new URLSearchParams(location.search).get("view") === "full");
  const reviewScroll = React.useRef(0);
  React.useEffect(() => {
    requestAnimationFrame(() => {
      const stage = document.querySelector(".stage");
      if (stage) stage.scrollTop = fullReview ? 0 : reviewScroll.current;
    });
  }, [fullReview]);
  const [rows, setRows] = React.useState<NodeRow[]>([]);
  const [edges, setEdges] = React.useState<any[]>([]);
  const [graphNodes, setGraphNodes] = React.useState<any[]>([]);
  const [contextRelations, setContextRelations] = React.useState<any[]>([]);
  const [judgeConfigured, setJudgeConfigured] = React.useState(false);
  const [workspaceLabel, setWorkspaceLabel] = React.useState("");
  const [selected, setSelected] = React.useState<string | null>(
    new URLSearchParams(location.search).get("conclusion_id"),
  );
  const [receipt, setReceipt] = React.useState<Receipt | null>(null);
  const selectionRequest = React.useRef(0);
  const decisionPending = React.useRef(false);
  const [eligible, setEligible] = React.useState<NodeRow[]>([]);
  const [contextLoading, setContextLoading] = React.useState(true);
  const [contextError, setContextError] = React.useState("");
  const [detailError, setDetailError] = React.useState("");
  const [reloadVersion, setReloadVersion] = React.useState(0);
  const scope = "";
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState("");
  const [csrf, setCsrf] = React.useState("");
  const csrfRef = React.useRef("");
  React.useEffect(() => { csrfRef.current = csrf; }, [csrf]);
  const [note, setNote] = React.useState("");
  const [busy, setBusy] = React.useState(false);
  const [decisionConfirmation, setDecisionConfirmation] = React.useState<{decision: string; id: string; statement: string; scope: string} | null>(null);
  const [revisionHandoff, setRevisionHandoff] = React.useState<any>(null);
  const cancelDecision = React.useRef<HTMLButtonElement>(null);
  const decisionTrigger = React.useRef<HTMLElement | null>(null);
  const [credentials, setCredentials] = React.useState<any[]>([]);
  const [activity, setActivity] = React.useState<any[]>([]);
  const [judgeConfirmation, setJudgeConfirmation] = React.useState(false);
  const [judgeMessage, setJudgeMessage] = React.useState("");
  const [credentialSecret, setCredentialSecret] = React.useState("");
  const [credentialsLoading, setCredentialsLoading] = React.useState(false);
  React.useEffect(() => {
    if (!receipt || !["queued", "running"].includes(receipt.judge_job?.state || "")) return;
    const id = receipt.conclusion.id;
    let active = true;
    const timer = window.setInterval(async () => {
      try { const next = await api(`/owner/api/conclusions/${encodeURIComponent(id)}`); if(active) setReceipt(previous=>previous?.conclusion.id===id?next:previous); }
      catch (e:any) { if(active) setError(`LM status could not refresh: ${e.message}`); }
    }, 2500);
    return ()=>{ active=false;window.clearInterval(timer); };
  }, [receipt?.conclusion.id,receipt?.judge_job?.state]);
  React.useEffect(() => {
    if (page !== "admin") return;
    let active = true;
    setCredentialsLoading(true);
    api("/v1/owner/credentials").then(body => {
      if (active) setCredentials(body.credentials || []);
    }).catch(e => { if (active) setError(e.message); })
      .finally(() => { if (active) setCredentialsLoading(false); });
    return () => { active = false; };
  }, [page, reloadVersion]);
  React.useEffect(() => {
    let active = true;
    api("/owner/api/activity").then(audit => { if (active) setActivity(audit); })
      .catch(e => { if (active) setError(`Activity could not load: ${e.message}`); });
    return () => { active = false; };
  }, [page, reloadVersion]);
  const load = React.useCallback(async () => {
    const request = ++selectionRequest.current;
    setLoading(true);
    setError("");
    setDetailError("");
    setReceipt(null);
    try {
      const [graph, session] = await Promise.all([
        api("/owner/api/graph"),
        api("/owner/api/session"),
      ]);
      const next = (graph.nodes || []).filter(
        (n: NodeRow) => n.type === "conclusion",
      );
      setRows(next);
      setGraphNodes(graph.nodes || []);
      setEdges(graph.edges || []);
      setJudgeConfigured(Boolean(session.capabilities?.judge));
      setWorkspaceLabel(session.workspace || "Owner workspace");
      setCsrf(session.csrf);
      const desired =
        selected && next.some((n: NodeRow) => n.id === selected)
          ? selected
          : next.find((n: NodeRow) => n.state === "needs_review")?.id ||
            null;
      if (request === selectionRequest.current) {
        setSelected(desired);
        setReceipt(null);
        if (desired) {
          const detail = await api(`/owner/api/conclusions/${encodeURIComponent(desired)}`);
          if (request === selectionRequest.current) setReceipt(detail);
        }
      }
    } catch (e: any) {
      setError(e.message);
      setDetailError(e.message);
    } finally {
      setLoading(false);
    }
  }, [selected]);
  React.useEffect(() => {
    load();
  }, []);
  React.useEffect(() => {
    let active = true;
    setEligible([]);
    setContextLoading(true);
    setContextError("");
    api(`/owner/api/context?scope=${encodeURIComponent(scope)}`).then(context => {
      if (active) { setContextRelations(context.relations || []); setEligible((context.knowledge || []).map((row: any) => ({
        ...row, label: row.statement, type: "conclusion", state: "admitted",
      }))); }
    }).catch(e => { if (active) { setContextError(e.message); setError(e.message); } })
      .finally(() => { if (active) setContextLoading(false); });
    return () => { active = false; };
  }, [scope, rows, reloadVersion]);
  React.useEffect(() => {
    const ctx =
      (document as any).modelContext || (navigator as any).modelContext;
    if (!ctx?.registerTool) return;
    const toolText = (value: unknown) => ({
      content: [{ type: "text", text: JSON.stringify(value, null, 2) }],
    });
    const tools = [
      {
        name: "get_workspace_summary",
        description: "Summarize the signed-in workspace, review queue, and current governed knowledge without changing state.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: {} },
        execute: async () => {
          const [graph, context, summary] = await Promise.all([api("/owner/api/graph"), api("/owner/api/context"), api("/owner/api/summary")]);
          const conclusions = (graph.nodes || []).filter((node: any) => node.type === "conclusion");
          return toolText({
            review: summary,
            current_knowledge_count: (context.knowledge || []).length,
            conclusion_states: conclusions.reduce((counts: Record<string, number>, row: any) => { counts[row.state] = (counts[row.state] || 0) + 1; return counts; }, {}),
            authority: "Agents may inspect and prepare work. Human Approval is not exposed.",
          });
        },
      },
      {
        name: "list_review_queue",
        description: "List candidate conclusions by review state and optional scope. This is a read-only queue view.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: { state: { type: "string", enum: ["needs_review", "needs_revision", "admitted", "rejected", "all"] }, scope: { type: "string" }, limit: { type: "integer", minimum: 1, maximum: 100 } } },
        execute: async ({ state = "needs_review", scope = "", limit = 25 }: any) => {
          const graph = await api(`/owner/api/graph?scope=${encodeURIComponent(scope)}`);
          const conclusions = (graph.nodes || []).filter((node: any) => node.type === "conclusion" && (state === "all" || node.state === state)).slice(0, limit).map(({ id, label, state, scope, created_at, proposer }: any) => ({ id, statement: label, state, scope, created_at, proposer }));
          return toolText({ conclusions, count: conclusions.length, open_in_review: `${location.origin}/review` });
        },
      },
      {
        name: "get_current_context",
        description:
          "Retrieve eligible governed conclusions for a scope. Does not approve knowledge.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: {
          type: "object",
          properties: { scope: { type: "string" }, task: { type: "string" } },
          required: ["scope"],
        },
        execute: async ({ scope, task }: any) =>
          toolText(
            await api(
              `/owner/api/context?scope=${encodeURIComponent(scope)}&task=${encodeURIComponent(task || "")}`,
            ),
          ),
      },
      {
        name: "get_review_state",
        description:
          "Inspect checks, advisory recommendation, and human-decision state. Does not approve.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: {
          type: "object",
          properties: { conclusion_id: { type: "string" } },
          required: ["conclusion_id"],
        },
        execute: async ({ conclusion_id }: any) =>
          toolText(
            await api(
              `/owner/api/conclusions/${encodeURIComponent(conclusion_id)}`,
            ),
          ),
      },
      {
        name: "get_lineage",
        description:
          "Inspect the evidence and decision history bound to a conclusion.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: {
          type: "object",
          properties: { conclusion_id: { type: "string" } },
          required: ["conclusion_id"],
        },
        execute: async ({ conclusion_id }: any) => {
          const r = await api(
            `/owner/api/conclusions/${encodeURIComponent(conclusion_id)}`,
          );
          return toolText({
            conclusion: r.conclusion,
            state: r.state,
            evidence: r.evidence,
            history: r.history,
          });
        },
      },
      {
        name: "run_deterministic_checks",
        description: "Run deterministic integrity and policy-prerequisite checks for one candidate. This appends evaluation receipts but cannot approve knowledge.",
        annotations: { readOnlyHint: false, untrustedContentHint: true },
        inputSchema: { type: "object", properties: { conclusion_id: { type: "string" } }, required: ["conclusion_id"] },
        execute: async ({ conclusion_id }: any) => {
          await api("/owner/api/evaluate", { method: "POST", body: JSON.stringify({ csrf: csrfRef.current, conclusion_id }) });
          const result = await api(`/owner/api/conclusions/${encodeURIComponent(conclusion_id)}`);
          setReloadVersion(version => version + 1);
          return toolText({ conclusion_id, evaluation: result.evaluation, human_approval_recorded: false, next: result.review_policy?.require_judge ? "LM advice is required by policy before Human Approval." : "Open the review surface for the owner decision." });
        },
      },
      {
        name: "open_review",
        description: "Open a conclusion in the owner review surface. Navigation does not make a decision.",
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        inputSchema: { type: "object", properties: { conclusion_id: { type: "string" }, full: { type: "boolean" } }, required: ["conclusion_id"] },
        execute: async ({ conclusion_id, full = true }: any) => {
          setSelected(conclusion_id); setPage("review"); setFullReview(Boolean(full));
          return toolText({ opened: true, decision_recorded: false, url: `${location.origin}/review?conclusion_id=${encodeURIComponent(conclusion_id)}${full ? "&view=full" : ""}` });
        },
      },
      {
        name: "prepare_review_response",
        description:
          "Prepare instructions for an agent to answer a clarification request through its agent credential. This owner-page tool does not submit or approve.",
        inputSchema: {
          type: "object",
          properties: {
            conclusion_id: { type: "string" },
            response: { type: "string" },
          },
          required: ["conclusion_id", "response"],
        },
        execute: async ({ conclusion_id, response }: any) =>
          toolText({
            conclusion_id,
            response,
            prepared: true,
            recorded: false,
            admitted: false,
            next: "Use the connected agent MCP or CLI to submit supporting evidence and a revision proposal; Human Approval remains separate.",
          }),
      },
      {
        name: "get_activity",
        description:
          "Read semantic workspace activity and knowledge-consumption receipts. Does not return provider secrets or owner credentials.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: {
          type: "object",
          properties: { limit: { type: "integer", minimum: 1, maximum: 100 } },
        },
        execute: async ({ limit = 50 }: any) =>
          toolText(await api(`/owner/api/activity?limit=${encodeURIComponent(String(limit))}`)),
      },
      {
        name: "get_review_policy",
        description:
          "Read the active workspace review policy and safe provider-configuration status. Secret values are never returned.",
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        inputSchema: { type: "object", properties: {} },
        execute: async () => toolText(await api("/owner/api/review-policy")),
      },
      {
        name: "prepare_review_policy_change",
        description:
          "Prepare a review-policy change in Admin for the human owner to inspect and activate. This never saves or authorizes the change.",
        annotations: { readOnlyHint: false, untrustedContentHint: false },
        inputSchema: {
          type: "object",
          properties: {
            provider: { type: "string", enum: ["openrouter", "openai", "anthropic", "custom"] },
            endpoint: { type: "string" },
            model: { type: "string" },
            criteria: { type: "string", maxLength: 8000 },
            zdr: { type: "boolean" },
            mode: { type: "string", enum: ["off", "manual", "automatic"] },
            require_judge: { type: "boolean" },
            external_consent: { type: "boolean" },
          },
          required: ["provider", "endpoint", "model", "criteria", "zdr", "mode", "require_judge", "external_consent"],
        },
        execute: async (settings: any) => {
          sessionStorage.setItem("proofpress:review-policy-draft", JSON.stringify(settings));
          navigate("admin");
          return toolText({
            prepared: true,
            activated: false,
            requires_human_owner: true,
            next: "Review the prepared settings in Admin, add a provider key if needed, then select Save & activate.",
            url: `${location.origin}/admin`,
          });
        },
      },
      {
        name: "get_agent_access",
        description: "List agent identities and credential lifecycle metadata. Credential secrets are never returned.",
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        inputSchema: { type: "object", properties: {} },
        execute: async () => {
          const result = await api("/v1/owner/credentials");
          return toolText({ credentials: (result.credentials || []).map(({ credential_id, principal_id, label, role, created_at, revoked_at }: any) => ({ credential_id, principal_id, label, role, created_at, revoked_at })) });
        },
      },
      {
        name: "prepare_agent_credential_issue",
        description: "Prepare an agent identity and key label in Admin. The human owner must issue the credential; no secret is exposed to the agent.",
        annotations: { readOnlyHint: false, untrustedContentHint: false },
        inputSchema: { type: "object", properties: { principal_id: { type: "string" }, label: { type: "string" } }, required: ["principal_id", "label"] },
        execute: async ({ principal_id, label }: any) => {
          sessionStorage.setItem("proofpress:agent-credential-draft", JSON.stringify({ principal_id, label }));
          navigate("admin");
          return toolText({ prepared: true, issued: false, requires_human_owner: true, secret_exposed_to_agent: false, url: `${location.origin}/admin` });
        },
      },
    ];
    Promise.all(tools.map((tool) => ctx.registerTool(tool))).catch(
      () => undefined,
    );
  }, []);
  React.useEffect(() => {
    history.replaceState(
      history.state,
      "",
      `/${page}${page === "review" && selected ? `?conclusion_id=${encodeURIComponent(selected)}${fullReview ? "&view=full" : ""}` : ""}`,
    );
  }, [page, selected, fullReview]);
  function openFullReview() {
    if (fullReview) { document.querySelector(".stage")?.scrollTo({top: 0}); return; }
    reviewScroll.current = document.querySelector(".stage")?.scrollTop || 0;
    history.pushState({proofpressFullReview: true}, "", `/review?conclusion_id=${encodeURIComponent(selected || "")}&view=full`);
    setFullReview(true);
  }
  function backToReview() {
    if (history.state?.proofpressFullReview) { history.back(); return; }
    history.pushState(null, "", `/review?conclusion_id=${encodeURIComponent(selected || "")}`);
    setFullReview(false);
  }
  function navigate(next: Page) {
    if (next === page) return;
    if (next === "review") { ++selectionRequest.current; setSelected(null); setReceipt(null); }
    setFullReview(false);
    history.pushState(null, "", `/${next}`);
    setPage(next);
    requestAnimationFrame(() => { document.querySelector(".stage")?.scrollTo({top:0}); window.scrollTo({top:0}); });
  }
  React.useEffect(() => {
    const restore = () => {
      const next = location.pathname.split("/")[1] as Page;
      setPage(labels[next] ? next : "review");
      setFullReview(new URLSearchParams(location.search).get("view") === "full");
      const id = new URLSearchParams(location.search).get("conclusion_id");
      if (id) void choose(id);
      else { ++selectionRequest.current; setSelected(null); setReceipt(null); setDetailError(""); }
    };
    window.addEventListener("popstate", restore);
    return () => window.removeEventListener("popstate", restore);
  }, []);
  async function choose(id: string) {
    if (decisionPending.current) return;
    if (selected === id && receipt?.conclusion.id === id) return;
    const request = ++selectionRequest.current;
    setSelected(id);
    setReceipt(null);
    setNote("");
    setError("");
    setDetailError("");
    try {
      const detail = await api(`/owner/api/conclusions/${encodeURIComponent(id)}`);
      if (request === selectionRequest.current) setReceipt(detail);
    } catch (e: any) {
      if (request === selectionRequest.current) { setError(e.message); setDetailError(e.message); }
    }
  }
  async function decide(decision: string, confirmed = false) {
    if (decisionPending.current || !receipt || receipt.conclusion.id !== selected) return;
    if (["admit", "reject"].includes(decision) && !confirmed) {
      decisionTrigger.current = document.activeElement as HTMLElement;
      setError("");
      setDecisionConfirmation({decision, id: receipt.conclusion.id, statement: receipt.conclusion.statement, scope: receipt.conclusion.scope || "this workspace"});
      return;
    }
    if (decision === "request_changes" && !note.trim()) {
      setError("Describe the bounded change the proposer should make.");
      return;
    }
    decisionPending.current = true;
    setBusy(true);
    try {
      const next = await api("/owner/api/reviews", {
        method: "POST",
        body: JSON.stringify({ csrf, conclusion_id: selected, decision, note }),
      });
      setReceipt(next);
      setDecisionConfirmation(null);
      setNote("");
      await load();
      if (decision === "request_changes") setRevisionHandoff(next);
    } catch (e: any) {
      setError(e.message);
    } finally {
      decisionPending.current = false;
      setBusy(false);
    }
  }
  async function runJudge() {
    if (!receipt || decisionPending.current) return;
    setJudgeConfirmation(false);
    decisionPending.current = true;
    setBusy(true);
    setError("");
    setJudgeMessage("Reviewing bound evidence… You can keep reading this conclusion.");
    try {
      await api("/owner/api/judge", {method: "POST", body: JSON.stringify({csrf, conclusion_id: receipt.conclusion.id, confirmed: true})});
      const next = await api(`/owner/api/conclusions/${encodeURIComponent(receipt.conclusion.id)}`);
      setReceipt(next);
      setJudgeMessage("LM advice recorded. See Checks for the reasoning.");
    } catch { setJudgeMessage("LM review did not complete. You can retry; no approval was recorded."); }
    finally { decisionPending.current = false; setBusy(false); }
  }
  async function runChecks() {
    if (!receipt || decisionPending.current) return;
    decisionPending.current = true; setBusy(true); setError("");
    try {
      await api("/owner/api/evaluate", {method:"POST",body:JSON.stringify({csrf,conclusion_id:receipt.conclusion.id})});
      await load();
    } catch (e:any) { setError(e.message); }
    finally { decisionPending.current=false; setBusy(false); }
  }
  async function showAdmin() {
    navigate("admin");
    try {
      const body = await api("/v1/owner/credentials");
      setCredentials(body.credentials || []);
    } catch (e: any) {
      setCredentials([]);
      setError(e.message);
    }
  }
  async function credentialAction(
    action: string,
    values: Record<string, string>,
  ) {
    if ((action === "revoke" || action === "rotate") && !window.confirm(
      action === "revoke" ? "Revoke this agent credential? Its access will stop immediately." : "Rotate this credential? The old credential will stop working."
    )) return;
    setBusy(true);
    setError("");
    try {
      const result = await api("/v1/owner/credentials", {
        method: "POST",
        body: JSON.stringify({ action, csrf, ...values }),
      });
      if (result.token) setCredentialSecret(result.token);
      await showAdmin();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  const pending = rows.filter((r) => r.state === "needs_review").length;
  const admitted = contextLoading ? "…" : eligible.length;
  return (
    <div className="shell" aria-busy={busy || loading}>
      <Dialog.Root open={Boolean(decisionConfirmation)} onOpenChange={open => { if (!open && !decisionPending.current) setDecisionConfirmation(null); }}>
          <ModalSurface onOpenAutoFocus={event => { event.preventDefault(); cancelDecision.current?.focus(); }} onCloseAutoFocus={event => { event.preventDefault(); if (decisionTrigger.current?.isConnected) decisionTrigger.current.focus(); }} onPointerDownOutside={event => event.preventDefault()} onEscapeKeyDown={event => { if (decisionPending.current) event.preventDefault(); }}>
            <Dialog.Title>{decisionConfirmation?.decision === "admit" ? "Approve this conclusion?" : "Reject this conclusion?"}</Dialog.Title>
            <Dialog.Description>{decisionConfirmation?.decision === "admit" ? "Eligible agents may rely on this conclusion within its scope. You are making the human approval decision." : "This decision will be recorded. The conclusion will remain excluded from governed context."}</Dialog.Description>
            <dl><dt>Scope</dt><dd>{decisionConfirmation?.scope}</dd></dl>
            <div className="confirmationStatement">{decisionConfirmation?.statement}</div>
            {error && <p role="alert">{error}</p>}
            <div className="confirmationActions">
              <Button ref={cancelDecision} variant="outline" disabled={busy} onClick={() => setDecisionConfirmation(null)}>Cancel</Button>
              <Button variant={decisionConfirmation?.decision === "admit" ? "approve" : "danger"} disabled={busy} onClick={() => {
                if (!decisionConfirmation) return;
                if (selected !== decisionConfirmation.id) { setError("The selected conclusion changed. Close this dialog and review it again."); return; }
                void decide(decisionConfirmation.decision, true);
              }}>{busy ? "Recording decision…" : decisionConfirmation?.decision === "admit" ? "Confirm approval" : "Confirm rejection"}</Button>
            </div>
          </ModalSurface>
      </Dialog.Root>
      <Dialog.Root open={Boolean(revisionHandoff)} onOpenChange={open => { if (!open) setRevisionHandoff(null); }}>
          <ModalSurface>
            <Dialog.Title>Changes requested</Dialog.Title>
            <Dialog.Description>Send the recorded change request to your agent.</Dialog.Description>
            {revisionHandoff && <RevisionInstructions receipt={revisionHandoff} autoCopy />}
            <div className="confirmationActions"><Button variant="outline" onClick={() => setRevisionHandoff(null)}>Close</Button><Button onClick={() => { setRevisionHandoff(null); openFullReview(); }}>View revision request</Button></div>
          </ModalSurface>
      </Dialog.Root>
      <aside className="sidebar">
        <div className="brand">
          <span className="brandMark"><img src="/logo.svg" alt="" /></span>
          <strong>Proofpress</strong>
        </div>
        <nav>
          {(Object.keys(labels) as Page[]).map((id) => {
            const Icon = icons[id];
            return (
              <button
                key={id}
                aria-label={labels[id]}
                aria-current={page === id ? "page" : undefined}
                className={page === id ? "active" : ""}
                onClick={() => navigate(id)}
              >
                <Icon />
                <span>{labels[id]}</span>
                {id === "review" && pending > 0 && <em>{pending}</em>}
              </button>
            );
          })}
        </nav>
        <div className="workspace">
          <span>WORKSPACE</span>
          <b>{workspaceLabel}</b>
          <small>Single-owner governance</small>
        </div>
      </aside>
      <main>
        <header className="topbar">
          <div className="mobileBrand">
            <span className="brandMark"><img src="/logo.svg" alt="" /></span>
            <strong>Proofpress</strong>
          </div>
          <span className="workspaceLabel">{workspaceLabel} · {labels[page]}</span>
        </header>
        {error && (
          <div className="error" role="alert">
            <span>{error}</span>
            {error.includes("session has expired") ? <a href={location.pathname + location.search}>Sign in again</a> : <button disabled={busy} onClick={() => { setReloadVersion(v => v + 1); void load(); }}>Reload workspace</button>}
            <button aria-label="Dismiss error" onClick={() => setError("")}>
              <X />
            </button>
          </div>
        )}
        <section className="stage">
          {page === "home" && (
            <HomePage
              pending={pending}
              admitted={admitted}
              rows={rows}
              onChoose={(id: string) => { navigate("review"); choose(id); }}
              onReview={() => navigate("review")}
              onLedger={() => navigate("ledger")}
            />
          )}
          {page === "review" && (
            <ReviewPage
              rows={rows}
              fullReview={fullReview}
              onOpenFull={openFullReview}
              onBack={backToReview}
              selected={selected}
              receipt={receipt}
              loading={loading}
              onChoose={choose}
              onClose={() => {
                ++selectionRequest.current;
                setSelected(null);
                setReceipt(null);
              }}
              note={note}
              setNote={setNote}
              onDecide={decide}
              busy={busy}
              onJudge={judgeConfigured ? () => setJudgeConfirmation(true) : undefined}
              onEvaluate={runChecks}
              onConfigurePolicy={showAdmin}
            />
          )}
          {page === "ledger" && (
            <LedgerPage
              rows={eligible}
              allRows={rows}
              nodes={graphNodes}
              edges={edges}
              relations={contextRelations}
              onReview={() => navigate("review")}
              contextError={contextError}
              detailError={detailError}
              loading={contextLoading}
              selected={selected}
              receipt={receipt}
              onChoose={choose}
            />
          )}
          {page === "activity" && <ActivityPage rows={activity} />}
          {page === "admin" && (
            <AdminPage
              policy={<ReviewPolicy csrf={csrf} api={api} onSaved={() => { void load(); }} />}
              credentials={credentials}
              loading={credentialsLoading}
              secret={credentialSecret}
              busy={busy}
              onAction={credentialAction}
              onDismissSecret={() => setCredentialSecret("")}
            />
          )}
        </section>
      </main>
      {judgeMessage && page === "review" && <div className="judgeProgress" role="status">{judgeMessage}<button aria-label="Dismiss LM review status" onClick={()=>setJudgeMessage("")}><X /></button></div>}
      <Dialog.Root open={judgeConfirmation} onOpenChange={setJudgeConfirmation}>
        <ModalSurface><Dialog.Title>Review evidence with LM</Dialog.Title><Dialog.Description>Send this conclusion and its bound evidence text to <strong>{receipt?.review_policy?.model || "the configured model"}</strong>. The selected provider will process this data, and provider charges may apply. The result is advice, not authorization.</Dialog.Description><div className="modalActions"><Button variant="outline" onClick={()=>setJudgeConfirmation(false)}>Cancel</Button><Button onClick={runJudge}>Run LM review</Button></div></ModalSurface>
      </Dialog.Root>
    </div>
  );
}

function PageHead({
  eyebrow,
  title,
  description,
  action,
}: {
  eyebrow: string;
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="pageHead">
      <div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {action}
    </div>
  );
}
function HomePage({ pending, admitted, rows, onReview, onLedger, onChoose }: any) {
  return (
    <div className="pageBody">
      <PageHead eyebrow="" title="Your workspace" description="Review new conclusions. Trace what agents may rely on." />
      <div className="orientation">
        <button onClick={onReview}>
          <span>Needs your review</span>
          <strong>{pending}</strong>
          <small>Candidate conclusions remain excluded</small>
          <ChevronRight />
        </button>
        <button onClick={onLedger}>
          <span>Current ledger</span>
          <strong>{admitted}</strong>
          <small>Current knowledge eligible for your owner identity</small>
          <BookOpen />
        </button>
      </div>
      <section className="section">
        {rows.some((r: any) => r.state === "needs_revision") && <button className="revisionQueueLink" onClick={() => onChoose(rows.find((r: any) => r.state === "needs_revision").id)}>{rows.filter((r: any) => r.state === "needs_revision").length} awaiting agent revision <ChevronRight /></button>}
        <div className="sectionTitle">
          <h2>Recent knowledge</h2>
          <span>{rows.length} total conclusions</span>
        </div>
        <div className="simpleList">
          {rows.slice(0, 6).map((r: any) => (
            <div key={r.id} role="button" tabIndex={0} onClick={() => onChoose(r.id)} onKeyDown={e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onChoose(r.id); } }}>
              <Badge state={r.state} />
              <b>{r.label}</b>
              <small>{r.scope || "Workspace"}</small>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
function ReviewPage({
  rows,
  selected,
  receipt,
  loading,
  onChoose,
  onClose,
  note,
  setNote,
  onDecide,
  busy,
  onJudge, onEvaluate,
  fullReview, onOpenFull, onBack,
}: any) {
  const [queue, setQueue] = React.useState("needs_review");
  const queueFor = (state: string) => state === "unresolved" ? "needs_review" : ["needs_review", "needs_revision"].includes(state) ? state : "decided";
  React.useEffect(() => { if (selected && receipt?.conclusion.id === selected) setQueue(queueFor(receipt.state)); }, [selected, receipt?.state]);
  const visibleRows = rows.filter((row: any) => queueFor(row.state) === queue);
  const switchQueue = (next: string) => { onClose(); setQueue(next); };
  return (
    <div className={`workspacePage reviewWorkspace${selected ? "" : " overviewOnly"}${fullReview ? " fullReviewPage" : ""}`}>
      <div className="work" style={fullReview ? {display: "none"} : undefined}>
        <PageHead
          eyebrow="GOVERNANCE INBOX"
          title="Review"
          description="Evidence and recommendations inform the decision. Only your approval admits knowledge."
        />
        <div className="filterbar">
          <Button variant={queue === "needs_review" ? "default" : "outline"} onClick={() => switchQueue("needs_review")}>Needs review</Button>
          <Button variant={queue === "needs_revision" ? "default" : "outline"} onClick={() => switchQueue("needs_revision")}>Needs revision</Button>
          <Button variant={queue === "decided" ? "default" : "outline"} onClick={() => switchQueue("decided")}>Decision history</Button>
          <span role="status">{loading ? "Loading review queue…" : `${visibleRows.length} conclusions`}</span>
        </div>
        <div className="tableWrap">
          <table>
            <thead>
              <tr>
                <th>Conclusion</th>
                <th>Status</th>
                <th>Scope</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {visibleRows.map((row: any) => (
                <tr
                  key={row.id}
                  className={selected === row.id ? "selected" : ""}
                  onClick={() => onChoose(row.id)}
                >
                  <td>
                    <button className="conclusionSelect" onClick={e => { e.stopPropagation(); onChoose(row.id); }}>{row.label}</button>
                    <small>{row.id}</small>
                  </td>
                  <td><Badge state={row.state} /></td>
                  <td>{row.scope || "—"}</td>
                  <td>
                    <ChevronRight />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!loading && visibleRows.length === 0 && (
            <div className="empty">{queue === "needs_review" ? "Nothing needs your review." : queue === "needs_revision" ? "No changes requested." : "No decisions recorded."}</div>
          )}
        </div>
      </div>
      <Inspector
        pending={!!selected && !receipt}
        receipt={receipt && visibleRows.some((row: any) => row.id === selected) ? receipt : null}
        onClose={onClose}
        note={note}
        setNote={setNote}
        onDecide={onDecide}
        busy={busy}
        onJudge={onJudge}
        onEvaluate={onEvaluate}
        fullReview={fullReview}
        onOpenFull={onOpenFull}
        onBack={onBack}
        onChoose={onChoose}
      />
    </div>
  );
}
function Inspector({
  receipt: r,
  onClose,
  note,
  setNote,
  onDecide,
  busy,
  onJudge, onEvaluate,
  readOnly = false,
  fullReview = false, onOpenFull, onBack, onChoose, onConfigurePolicy, pending = false,
}: any) {
  const [expanded, setExpanded] = React.useState(false);
  const panel = React.useRef<HTMLElement>(null);
  React.useEffect(() => {
    setExpanded(false);
    panel.current?.scrollTo({top: 0, behavior: "auto"});
  }, [r?.conclusion.id]);
  React.useEffect(() => {
    if (!r || !window.matchMedia("(max-width: 1050px)").matches) return;
    const opener = document.querySelector<HTMLElement>(".work tr.selected .conclusionSelect") || document.activeElement as HTMLElement | null;
    panel.current?.querySelector<HTMLButtonElement>(".mobileBack")?.focus();
    return () => { requestAnimationFrame(() => { if (opener?.isConnected && opener !== document.body) opener.focus(); }); };
  }, [r?.conclusion.id]);
  if (!r) return pending ? <aside className="inspector" aria-label="Conclusion details" aria-busy="true"><div className="inspectorTop" role="status">Loading details…</div></aside> : null;
  const can = ["needs_review", "unresolved"].includes(r.state) && !readOnly;
  const failedChecks = Object.entries(r.evaluation?.checks || {}).filter(([,passed])=>!passed).map(([key])=>key.replaceAll("_", " "));
  const checkReason = (name:string) => ({"evidence present":"Required evidence is missing","evidence integrity":"Evidence integrity could not be verified","experiment evidence present":"Typed experiment evidence is missing","experiment evidence valid":"Experiment evidence is incomplete or invalid","experiment identity bound":"Experiment identity is not bound","not expired":"The conclusion has expired","not superseded":"The conclusion was superseded","scope present":"A reuse scope is missing"} as Record<string,string>)[name] || `${name} did not pass`;
  const checksMissing = !r.evaluation || (r.review_policy && !r.review_policy.checks_current);
  const judgeNeedsSetup = r.review_policy?.mode === "off";
  const judgePending = r.review_policy?.mode !== "off" && !r.recommendation;
  const judgeFailed = ["failed", "interrupted"].includes(r.judge_job?.state);
  const approvalBlock = !r.evaluation ? "Run deterministic checks before approval." : failedChecks.length ? failedChecks.map(checkReason).join(". ") + "." : r.review_policy && !r.review_policy.checks_current ? "Review policy changed. Run checks again before approval." : r.review_policy?.require_judge && (!r.review_policy.advice_current || r.recommendation?.recommendation !== "accept") ? "Current, supporting LM advice is required before approval." : "";
  return (
    <aside className={`inspector${fullReview ? " fullReview" : ""}`} ref={panel} aria-label="Conclusion details" onKeyDown={e => { if (e.key === "Escape" && onClose) { e.stopPropagation(); fullReview ? onBack() : onClose(); } }}>
      {!can && !readOnly && <DecisionNotice state={r.state}>{r.state === "blocked" && <p>Deterministic requirements did not pass. This candidate is excluded from LM and human review.</p>}</DecisionNotice>}
      {fullReview && <Button variant="outline" onClick={onBack}>Back to review</Button>}
      {!fullReview && onClose && <button className="mobileBack" onClick={onClose}>
        Close details
      </button>}
      <div className="inspectorTop">
        <Badge state={r.state} />
        {r.state === "unresolved" && <p>Previous approval needs revalidation under the current policy.</p>}
        <h2>{r.conclusion.statement}</h2>
        <p>
          Proposed by {r.conclusion.proposer || "agent"} ·{" "}
          <span className="mono">{r.conclusion.id}</span>
        </p>
      </div>
      {r.revision_request && <RevisionPanel receipt={r} onChoose={onChoose} />}
      <div className="quickSnapshot">
        <dl><div><dt>Applies to</dt><dd>{r.conclusion.scope || "No scope recorded"}</dd></div>
        <div><dt>Supporting evidence</dt><dd>{(r.evidence || []).length} bound {(r.evidence || []).length === 1 ? "source" : "sources"}</dd></div>
        <div><dt>Automated checks</dt><dd className={r.evaluation ? (failedChecks.length ? "checkSummary fail" : "checkSummary pass") : ""}>{Object.keys(r.evaluation?.checks || {}).length ? `${Object.values(r.evaluation.checks).filter(Boolean).length} of ${Object.keys(r.evaluation.checks).length} passed` : "Not run"}</dd></div>
        <div><dt>LM advice</dt><dd>{r.recommendation ? <Badge state={r.recommendation.recommendation} /> : r.judge_job?.state === "running" || r.judge_job?.state === "queued" ? "Review in progress" : judgeFailed ? "Review failed" : judgeNeedsSetup || !onJudge ? "Policy setup required" : "Not run yet"}</dd></div></dl>
        {can && <div className="decisionStack"><div><strong>Automated checks</strong><span className={r.evaluation ? (failedChecks.length ? "fail" : "pass") : ""}>{approvalBlock && failedChecks.length ? `Blocking · ${failedChecks.length} requirement${failedChecks.length===1?"":"s"} failed` : r.evaluation ? "Passed" : "Not run"}</span></div><div><strong>LM advice</strong><span>{r.recommendation ? `${r.recommendation.recommendation === "accept" ? "Supports the evidence" : r.recommendation.recommendation} · advisory only` : "Not recorded"}</span></div><div><strong>Human authorization</strong><span>{approvalBlock ? "Unavailable until requirements pass" : "Ready for your decision"}</span></div></div>}
        {can && approvalBlock && <p className="approvalBlock" role="status">{approvalBlock}</p>}
        {r.judge_job && ["failed","interrupted","blocked"].includes(r.judge_job.state) && <p>{r.judge_job.detail}</p>}
        {can && <div className="reviewActions">
          {checksMissing && onEvaluate ? <Button disabled={busy} onClick={onEvaluate}>Run deterministic checks</Button>
            : failedChecks.length ? <span className="blockedAction">Not eligible for human review</span>
            : (judgeNeedsSetup || !onJudge) && onConfigurePolicy ? <Button onClick={onConfigurePolicy}>Configure review policy</Button>
            : judgeFailed && onJudge ? <Button disabled={busy} onClick={onJudge}>Retry LM review</Button>
            : judgePending && r.review_policy?.mode === "automatic" ? <span className="queuedAction">LM review runs automatically after checks</span>
            : judgePending && onJudge && r.review_policy?.mode === "manual" ? <Button disabled={busy} onClick={onJudge}>Run LM review</Button>
            : onOpenFull && !fullReview ? <Button onClick={onOpenFull}>Open full review</Button>
            : null}
          {!checksMissing && !failedChecks.length && onOpenFull && !fullReview && ((judgeNeedsSetup && onConfigurePolicy) || (judgePending && r.review_policy?.mode === "manual" && onJudge)) && <Button className="secondaryAction" variant="ghost" onClick={onOpenFull}>Open full review</Button>}
          {r.recommendation && onJudge && r.review_policy?.mode === "manual" && <Button className="secondaryAction" variant="ghost" disabled={busy} onClick={onJudge}>Refresh LM advice</Button>}
        </div>}
        {!can && (onOpenFull ? !fullReview && <Button onClick={onOpenFull}>{r.state === "needs_revision" ? "View revision request" : "View decision"}</Button> : <Button variant="outline" aria-expanded={expanded} onClick={() => setExpanded(!expanded)}>{expanded ? "Hide details" : "View details"}</Button>)}
      </div>
      {(fullReview || expanded) && <>
      {r.revision_parent && <section className="revisionSection"><h3>Revision of previous conclusion</h3><p>{r.revision_parent.statement}</p><p><b>Requested change:</b> {r.revision_parent.review?.note}</p><p>Previous evidence: {r.revision_parent.evidence_refs.join(", ")}</p><p>Current evidence: {r.conclusion.evidence_refs.join(", ")}</p><p>This proposal requires a new human decision; it does not automatically replace its predecessor.</p></section>}
      <Tabs.Root defaultValue="evidence">
        <Tabs.List className="tabs">
          <Tabs.Trigger value="evidence">Evidence</Tabs.Trigger>
          <Tabs.Trigger value="checks">Checks</Tabs.Trigger>
          <Tabs.Trigger value="history">History</Tabs.Trigger>
        </Tabs.List>
        <Tabs.Content value="evidence" className="tabContent">
          {(r.evidence || []).map((e: any, i: number) => (
            <article className="evidenceRow" key={i}>
              <div>
                <ShieldCheck />
                <b>{evidenceName(e)}</b>
              </div>
              <EvidenceContent row={e} />
              <small>Bound to this conclusion</small>
            </article>
          ))}
          {!(r.evidence || []).length && (
            <div className="empty">No bound evidence on this receipt.</div>
          )}
        </Tabs.Content>
        <Tabs.Content value="checks" className="tabContent">
          <div className="checkList">
            {!Object.keys(r.evaluation?.checks || {}).length && <p className="empty">No deterministic checks recorded.</p>}
            {Object.entries(r.evaluation?.checks || {}).map(
              ([key, value]: any) => (
                <div key={key}>
                  <span>{key.replaceAll("_", " ")}</span>
                  <b className={value ? "pass" : "fail"}>
                    {value ? (
                      <>
                        <Check />
                        Passed
                      </>
                    ) : (
                      "Failed"
                    )}
                  </b>
                </div>
              ),
            )}
          </div>
          <div className="recommendation">
            <span>LM advice</span>
            {r.recommendation ? <Badge state={r.recommendation.recommendation} /> : <b>No recommendation recorded</b>}
            {r.recommendation?.model && <small>{r.recommendation.model} · {r.recommendation.judge}</small>}
            <p>
              {r.recommendation?.rationale ||
                ""}
            </p>
          </div>
        </Tabs.Content>
        <Tabs.Content value="history" className="tabContent">
          {(r.history || []).map((h: any, i: number) => (
            <div className="historyRow" key={i}>
              <span></span>
              <div>
                <b>{h.type.replaceAll("_", " ")}</b>
                <p>{historyActor({...([r.evaluation, r.recommendation, r.review, r.admission, r.rejection].find(event => event?.event_id === h.event_id) || {}), ...(h.type === "conclusion_proposed" ? {conclusion:r.conclusion} : {}), ...h})}</p>
                {h.note && <p>{h.note}</p>}
                <small>{h.created_at}</small>
              </div>
            </div>
          ))}
        </Tabs.Content>
      </Tabs.Root>
      </>}
      {can && (!onOpenFull || fullReview) ? (
        <div className="decision">
          <textarea
            aria-label="Review note or bounded clarification request"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Review note or bounded clarification request"
          />
          <div>
            <Button
              variant="danger"
              disabled={busy}
              onClick={() => onDecide("reject")}
            >
              Reject
            </Button>
            <Button
              variant="outline"
              disabled={busy}
              onClick={() => onDecide("request_changes")}
            >
              Request changes
            </Button>
            <Button
              variant="approve"
              disabled={busy || !!approvalBlock}
              onClick={() => onDecide("admit")}
            >
              Approve for reuse
            </Button>
          </div>
        </div>
      ) : null}
    </aside>
  );
}
function LedgerPage({ rows, allRows, nodes, edges, relations, selected, receipt, onChoose, onReview, loading, contextError, detailError }: any) {
  const [view, setView] = React.useState("lineage");
  const [showHistory, setShowHistory] = React.useState(true);
  const [focused, setFocused] = React.useState(false);
  const [graphSelection, setGraphSelection] = React.useState("conclusion");
  const available = new Set(rows.map((row: any) => row.id));
  const visible = showHistory ? allRows : rows;
  const current = !loading && visible.some((row: any) => row.id === selected) && receipt?.conclusion.id === selected ? receipt : null;
  const visibleIds = new Set(visible.map((row: any) => row.id));
  const links = (showHistory ? edges : relations).filter((edge: any) => visibleIds.has(edge.from) && visibleIds.has(edge.to));
  const related = links.filter((edge: any) => edge.from === selected || edge.to === selected);
  const focus = (id: string) => { setFocused(true); setGraphSelection("conclusion"); onChoose(id); };
  React.useEffect(() => { setGraphSelection("conclusion"); }, [selected]);
  return (
    <div className={`workspacePage${focused ? "" : " overviewOnly"}`}>
      <div className="work">
        <PageHead
          eyebrow="GOVERNED CONTEXT"
          title="Ledger"
          description="Explore evidence and decisions across the workspace. Current knowledge shows only what is eligible for reuse."
        />
        <div className="ledgerViews" role="group" aria-label="Ledger view">
          <Button aria-pressed={view === "lineage"} variant="outline" onClick={() => setView("lineage")}>Lineage</Button>
          <Button aria-pressed={view === "list"} variant="outline" onClick={() => setView("list")}>Current knowledge</Button>
        </div>
        {view === "lineage" && <p className="graphScrollHint">Scroll sideways to explore the graph.</p>}
        {view === "lineage" && <section className="lineageCanvas" aria-label="Evidence to governed knowledge">
          <div className="lineageToolbar">
            {focused && <Button variant="outline" onClick={() => setFocused(false)}><ChevronRight style={{transform:"rotate(180deg)"}} />Back to overview</Button>}
            <label><input type="checkbox" checked={showHistory} onChange={e => { setShowHistory(e.target.checked); setFocused(false); }} /> Show history and unavailable conclusions</label>
          </div>
          {!focused && <LedgerOverview rows={visible} nodes={nodes} edges={edges} onChoose={focus} />}
          {focused && current ? <><LineageGraph receipt={current} available={available.has(selected)} evidenceNames={(current.evidence || []).map(evidenceName)} selection={graphSelection} onSelect={setGraphSelection} /><section className="relatedConclusions"><h2>Direct relations</h2>{related.length ? related.map((edge: any, i: number) => {
            const other = visible.find((row: any) => row.id === (edge.from === selected ? edge.to : edge.from));
            return <button key={edge.id || i} onClick={() => focus(other.id)}><span>{edge.from === selected ? "Outgoing" : "Incoming"} · {edge.type.replaceAll("_", " ")} · {edge.state || "recorded"}</span><b>{other.label}</b></button>;
          }) : <p>No recorded relations to other conclusions in this view.</p>}</section></> : focused && <div className="empty">{detailError ? <><p>Could not load this conclusion. No stale receipt is shown.</p><Button variant="outline" onClick={() => onChoose(selected)}>Retry details</Button></> : "Loading selected lineage…"}</div>}
        </section>}
        {view === "list" &&
        <div className="tableWrap">
          <table>
            <thead>
              <tr>
                <th>Current conclusion</th>
                <th>Scope</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r: any) => (
                <tr
                  key={r.id}
                  className={selected === r.id ? "selected" : ""}
                  onClick={() => focus(r.id)}
                >
                  <td>
                    <button className="conclusionSelect" onClick={e => { e.stopPropagation(); focus(r.id); }}>{r.label}</button>
                    <small>{r.id}</small>
                  </td>
                  <td>{r.scope || "—"}</td>
                  <td>
                    <Badge state={r.state} />
                  </td>
                  <td>
                    <ChevronRight />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {rows.length === 0 && (
            <div className="empty">
              {loading ? "Loading eligible knowledge…" : contextError ? "Current knowledge could not be loaded. Use Reload workspace to retry." : "No current knowledge is eligible for this scope and identity."}
            </div>
          )}
        </div>
        }
      </div>
      {focused && current && graphSelection !== "conclusion" ? <aside className="inspector graphInspector" aria-label="Selected node details"><Button variant="outline" onClick={() => setGraphSelection("conclusion")}>Back to conclusion</Button>{graphSelection === "context" ? <><h2>{available.has(selected) ? "Available for reuse" : "Excluded from context"}</h2><p>Scope: {current.conclusion.scope}</p><p>{available.has(selected) ? "Admitted, current, and eligible for the signed-in owner. Each agent's permissions are checked separately." : "This conclusion is not eligible for the current owner context."}</p></> : <><h2>{evidenceName(current.evidence[Number(graphSelection.split(":")[1])])}</h2><EvidenceContent row={current.evidence[Number(graphSelection.split(":")[1])]} /></>}</aside> : <Inspector
        receipt={focused ? current : null}
        pending={focused && !current && !detailError}
        onClose={() => setFocused(false)}
        readOnly
        note=""
        setNote={() => {}}
        onDecide={() => {}}
        busy={false}
      />}
    </div>
  );
}
function ActivityPage({ rows }: any) {
  const [page, setPage] = React.useState(0);
  const [view, setView] = React.useState("activity");
  const [logs, setLogs] = React.useState<any[]>([]);
  const [error, setError] = React.useState("");
  React.useEffect(() => {
    if (view !== "logs") return;
    let active = true;
    api("/owner/api/technical-logs").then(rows => { if(active) setLogs(rows); }).catch(e=>{ if(active) setError(e.message); });
    return ()=>{ active=false; };
  }, [view]);
  const filtered = view === "logs" ? logs : rows.filter((r:any)=>view!=="retrievals" || r.kind==="context_retrieved");
  const pages = Math.max(1, Math.ceil(filtered.length / 20));
  const current = Math.min(page, pages - 1);
  return (
    <div className="pageBody">
      <PageHead
        eyebrow="APPEND-ONLY RECORD"
        title="Activity"
        description="Who contributed knowledge, reviewed it, and retrieved context. Technical requests are kept separately."
      />
      <div className="ledgerViews activityFilters" role="group" aria-label="Activity filter">
        {[["activity","Knowledge activity"],["retrievals","Context retrievals"],["logs","Technical logs"]].map(([key,label])=><Button key={key} aria-pressed={view===key} onClick={()=>{setView(key);setPage(0);setError("");}}>{label}</Button>)}
      </div>
      {error && <p role="alert">{error}</p>}
      <div className="tableWrap activityTable">
        <table><caption className="sr-only">Recent workspace activity</caption><thead><tr><th>Time</th><th>{view==="logs"?"Operation":"What happened"}</th><th>Actor</th><th>Result</th></tr></thead><tbody>
        {filtered.slice(current * 20, (current + 1) * 20).map((r: any) => (
          <tr key={r.id || r.audit_id}>
            <td data-label="Time"><time dateTime={r.occurred_at} title={r.occurred_at}>{new Date(r.occurred_at).toLocaleString()}</time></td>
            <td data-label="What happened">{view==="logs" ? (r.operation || "request").replaceAll(".", " · ") : <><strong>{r.action}</strong>{r.statement && <a className="activitySubject" href={`/review?conclusion_id=${encodeURIComponent(r.subject_id)}&view=full`}>{r.statement}</a>}{r.detail && <details><summary>Details</summary><p>{r.detail}</p></details>}{r.scope && <small>{r.scope}</small>}</>}</td>
            <td data-label="Actor">{r.actor || r.principal_id || "Actor not recorded"}{r.model && <small>{r.model}</small>}{r.initiator && r.initiator!==r.actor && <small>Requested by {r.initiator}</small>}</td>
            <td data-label="Result">{view==="logs" ? <ActivityResult outcome={r.outcome} /> : <Badge state={r.outcome} />}</td>
          </tr>
        ))}
        </tbody></table>
        {!filtered.length && <p className="empty">{view==="retrievals"?"No context retrievals recorded yet. Historical reads remain in Technical logs.":"No activity records loaded."}</p>}
      </div>
      <nav className="pagination" aria-label="Activity pages">
        <Button variant="outline" disabled={current === 0} onClick={() => setPage(current - 1)}>Previous</Button>
        <span>Page {current + 1} of {pages} · {filtered.length} records</span>
        <Button variant="outline" disabled={current + 1 >= pages} onClick={() => setPage(current + 1)}>Next</Button>
      </nav>
    </div>
  );
}
function AdminPage({
  policy,
  credentials,
  loading,
  secret,
  busy,
  onAction,
  onDismissSecret,
}: any) {
  const [principal, setPrincipal] = React.useState("");
  const [label, setLabel] = React.useState("");
  const [copyStatus, setCopyStatus] = React.useState("");
  const [agentDraftLoaded, setAgentDraftLoaded] = React.useState(false);
  React.useEffect(() => setCopyStatus(""), [secret]);
  React.useEffect(() => {
    const raw = sessionStorage.getItem("proofpress:agent-credential-draft");
    if (!raw) return;
    try {
      const draft = JSON.parse(raw);
      setPrincipal(String(draft.principal_id || ""));
      setLabel(String(draft.label || ""));
      setAgentDraftLoaded(true);
    } finally {
      sessionStorage.removeItem("proofpress:agent-credential-draft");
    }
  }, []);
  return (
    <div className="pageBody">
      <PageHead
        eyebrow="OWNER ONLY"
        title="Admin"
        description="Manage the agents that can propose knowledge and read governed context."
        action={null}
      />
      {policy}
      {agentDraftLoaded && <DecisionNotice tone="info" title="Agent-prepared credential" detail="Review the agent identity and key name below. Nothing has been issued yet." />}
      <form
        className="issueForm"
        onSubmit={(event) => {
          event.preventDefault();
          onAction("issue", { principal_id: principal, label });
        }}
      >
        <div>
          <b>Issue agent credential</b>
          <small>
            Create a key for an agent or device. You can revoke its access later.
          </small>
        </div>
        <label>Agent identity<input
          aria-label="Agent identity"
          aria-describedby="agentIdentityHelp"
          value={principal}
          onChange={(e) => setPrincipal(e.target.value)}
          placeholder="agent:claude-code"
          required
        /><small id="agentIdentityHelp">Recorded as the author in history, e.g. agent:claude-code.</small></label>
        <label>Key name<input
          aria-label="Key name"
          aria-describedby="keyNameHelp"
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          placeholder="Claude Code · company laptop"
          required
        /><small id="keyNameHelp">A name you recognize, such as Claude Code · work laptop.</small></label>
        <Button disabled={busy}>Issue credential</Button>
      </form>
      {secret && (
        <div className="secretReveal">
          <div>
            <b>Copy this credential now</b>
            <p>
              It is shown once. Store it in the agent client's secure local
              configuration.
            </p>
            <code>{secret}</code>
          </div>
          <div>
            <Button
              variant="outline"
              onClick={async () => {
                try { await navigator.clipboard.writeText(secret); setCopyStatus("Copied"); }
                catch { setCopyStatus("Copy failed. Select the credential and copy it manually."); }
              }}
            >
              Copy
            </Button>
            <Button variant="ghost" onClick={onDismissSecret}>
              Done
            </Button>
          </div>
          {copyStatus && <p role="status">{copyStatus}</p>}
        </div>
      )}
      <div className="credentialList" aria-busy={loading}>
        {loading && !credentials.length && <p className="empty" role="status">Loading agent credentials…</p>}
        {credentials.map((c: any) => (
          <div key={c.credential_id}>
            <div className="credentialIcon">
              <KeyRound />
            </div>
            <div>
              <b>{c.label || c.principal_id}</b>
              <small>{c.principal_id}</small>
            </div>
            <Badge state={c.revoked_at ? "revoked" : "active"} />
            {!c.revoked_at && c.role === "agent" ? (
              <div className="credentialActions">
                <Button
                  variant="outline"
                  disabled={busy}
                  onClick={() =>
                    onAction("rotate", { credential_id: c.credential_id })
                  }
                >
                  Rotate
                </Button>
                <Button
                  variant="danger"
                  disabled={busy}
                  onClick={() =>
                    onAction("revoke", { credential_id: c.credential_id })
                  }
                >
                  Revoke
                </Button>
              </div>
            ) : (
              <span />
            )}
          </div>
        ))}
      </div>
      <div className="boundary">
        <ShieldCheck />
        <div>
          <b>Authority boundary</b>
          <p>
            Agent credentials can submit evidence, propose conclusions, and read
            admitted context. They cannot approve knowledge or change policy.
          </p>
        </div>
      </div>
    </div>
  );
}
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
