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
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { DecisionNotice, RevisionInstructions, RevisionPanel, historyActor } from "@/components/review-feedback";
import { KnowledgeLibrary } from "@/components/knowledge-library";
import { claimDisplayTitle, hasDistinctClaimHeading } from "@/components/claim-display";
import { ModalSurface } from "@/components/ui/modal-surface";
import "./index.css";
import "./review-local.css";
import "./components/governance.css";
import "./components/workspace-home.css";

type NodeRow = {
  id: string;
  type: string;
  label: string;
  title?: string;
  state: string;
  scope?: string;
  applicability?: Receipt["claim"]["applicability"];
  created_at?: string;
  decision_at?: string;
};
type Receipt = {
  state: string;
  claim: {
    id: string;
    statement: string;
    title?: string;
    evidence_refs: string[];
    reproposal_of?: string | null;
    qualifiers?: { reproposal_response?: string };
    scope?: string;
    proposer?: string;
    created_at?: string;
    applicability?: {
      title?: string;
      description?: string;
      when_relevant?: string[];
      keywords?: string[];
      validity_conditions?: string[];
    } | null;
  };
  evidence?: any[];
  evaluation?: { checks?: Record<string, boolean> };
  recommendation?: { recommendation?: string; rationale?: string };
  revision_request?: any;
  revision_parent?: {id:string;statement:string;evidence_refs:string[];review?:{note?:string}} | null;
  reproposal_parent?: {id:string;statement:string;evidence_refs:string[];new_evidence_refs?:string[];reused_evidence_refs?:string[];reproposal_response?:string;rejection_reason?:string;rejection?:{note?:string};review?:{note?:string}} | null;
  reproposals?: {id:string;statement:string;state:string}[];
  history?: any[];
  judge_job?: {state:string;detail:string};
  review_policy?: {require_judge:boolean;mode:string;model:string;rubric:string;checks_current:boolean;advice_current:boolean};
};
type Page = "home" | "review" | "ledger" | "runs" | "activity" | "admin";
const labels: Record<Page, string> = {
  home: "Home",
  review: "Review",
  ledger: "Knowledge",
  runs: "Runs",
  activity: "Activity",
  admin: "Admin",
};
const icons = {
  home: Home,
  review: ShieldCheck,
  ledger: BookOpen,
  runs: Activity,
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
function reuseBoundary(claim: Receipt["claim"]) {
  const card = claim.applicability;
  return card?.title || card?.description || claim.scope || "No reuse boundary recorded";
}

function ExpandableText({ text, label = "Show full text" }: { text: string; label?: string }) {
  const [open, setOpen] = React.useState(false);
  return <div className={`expandableText${open ? " expanded" : ""}`}>
    <p>{text}</p>
    <button type="button" aria-expanded={open} onClick={() => setOpen(!open)}>{open ? "Show less" : label}</button>
  </div>;
}

function EvidenceContent({ row, collapsible = false }: { row: any; collapsible?: boolean }) {
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
  return <>{structured !== null ? renderValue(structured) : collapsible ? <ExpandableText text={text} label="Show full excerpt" /> : <p>{text}</p>}
    <details className="technicalDetails"><summary>Technical receipt</summary><pre>{JSON.stringify(row, null, 2)}</pre></details>
  </>;
}

function CompactEvidenceExcerpt({ text }: { text: string }) {
  const [open, setOpen] = React.useState(false);
  const expandable = text.length > 220;
  return <div className={`compactEvidenceExcerpt${open ? " expanded" : ""}`}>
    <p>{text}</p>
    {expandable && <button type="button" aria-expanded={open} onClick={() => setOpen(!open)}>{open ? "Show less" : "Show full excerpt"}</button>}
  </div>;
}

function EvidencePreview({ row }: { row: any }) {
  const text = evidenceText(row);
  if (typeof text !== "string") return <CompactEvidenceExcerpt text={String(text)} />;
  try {
    const structured = JSON.parse(text);
    const preferred = ["finding", "summary", "result", "observation", "hypothesis", "decision"];
    const findExcerpt = (value: any, depth = 0): string | null => {
      if (!value || typeof value !== "object" || depth > 2) return null;
      for (const key of preferred) {
        const candidate = value[key];
        if (["string", "number", "boolean"].includes(typeof candidate)) return String(candidate);
      }
      for (const candidate of Object.values(value)) {
        const excerpt = findExcerpt(candidate, depth + 1);
        if (excerpt) return excerpt;
      }
      return null;
    };
    const excerpt = findExcerpt(structured);
    if (excerpt) return <CompactEvidenceExcerpt text={excerpt} />;
  } catch { /* Plain evidence remains readable prose. */ }
  return <CompactEvidenceExcerpt text={text} />;
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
    new URLSearchParams(location.search).get("claim_id"),
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
  const [pendingRejection, setPendingRejection] = React.useState<{id: string; note: string; nextId: string | null; seconds: number} | null>(null);
  const rejectTimeout = React.useRef<number | null>(null);
  const rejectCountdown = React.useRef<number | null>(null);
  const [revisionHandoff, setRevisionHandoff] = React.useState<any>(null);
  const cancelDecision = React.useRef<HTMLButtonElement>(null);
  const decisionTrigger = React.useRef<HTMLElement | null>(null);
  const [credentials, setCredentials] = React.useState<any[]>([]);
  const [activity, setActivity] = React.useState<any[]>([]);
  const [runs, setRuns] = React.useState<any[]>([]);
  const [selectedRun, setSelectedRun] = React.useState<any>(null);
  const [runsLoading, setRunsLoading] = React.useState(false);
  const [judgeConfirmation, setJudgeConfirmation] = React.useState(false);
  const [judgeMessage, setJudgeMessage] = React.useState("");
  const [judgeRunning, setJudgeRunning] = React.useState(false);
  const [credentialSecret, setCredentialSecret] = React.useState("");
  const [credentialsLoading, setCredentialsLoading] = React.useState(false);
  React.useEffect(() => () => {
    if (rejectTimeout.current !== null) window.clearTimeout(rejectTimeout.current);
    if (rejectCountdown.current !== null) window.clearInterval(rejectCountdown.current);
  }, []);
  React.useEffect(() => {
    if (!receipt || !["queued", "running"].includes(receipt.judge_job?.state || "")) return;
    const id = receipt.claim.id;
    let active = true;
    const timer = window.setInterval(async () => {
      try { const next = await api(`/owner/api/claims/${encodeURIComponent(id)}`); if(active) setReceipt(previous=>previous?.claim.id===id?next:previous); }
      catch (e:any) { if(active) setError(`LM status could not refresh: ${e.message}`); }
    }, 2500);
    return ()=>{ active=false;window.clearInterval(timer); };
  }, [receipt?.claim.id,receipt?.judge_job?.state]);
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
    if (page !== "runs") return;
    let active = true;
    setRunsLoading(true);
    api("/owner/api/runs").then(body => { if (active) setRuns(body.runs || []); })
      .catch(e => { if (active) setError(`Runs could not load: ${e.message}`); })
      .finally(() => { if (active) setRunsLoading(false); });
    return () => { active = false; };
  }, [page, reloadVersion]);
  React.useEffect(() => {
    let active = true;
    api("/owner/api/activity").then(audit => { if (active) setActivity(audit); })
      .catch(e => { if (active) setError(`Activity could not load: ${e.message}`); });
    return () => { active = false; };
  }, [page, reloadVersion]);
  const load = React.useCallback(async (selectionOverride?: string | null) => {
    const targetSelection = selectionOverride === undefined ? selected : selectionOverride;
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
        (n: NodeRow) => n.type === "claim",
      );
      setRows(next);
      setGraphNodes(graph.nodes || []);
      setEdges(graph.edges || []);
      setJudgeConfigured(Boolean(session.capabilities?.judge));
      setWorkspaceLabel(session.workspace || "Owner workspace");
      setCsrf(session.csrf);
      const selectedExists = Boolean(targetSelection && next.some((n: NodeRow) => n.id === targetSelection));
      const desired = targetSelection
        ? selectedExists ? targetSelection : null
        : next.find((n: NodeRow) => n.state === "needs_review")?.id || null;
      if (request === selectionRequest.current) {
        setReceipt(null);
        if (targetSelection && !selectedExists) {
          setDetailError("This claim was not found. No substitute receipt has been shown.");
          return;
        }
        setSelected(desired);
        if (desired) {
          const detail = await api(`/owner/api/claims/${encodeURIComponent(desired)}`);
          if (request === selectionRequest.current) setReceipt(detail);
        }
      }
    } catch (e: any) {
      if (targetSelection) setDetailError(e.message);
      else setError(e.message);
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
      if (active) { setContextRelations(context.relations || []); setEligible((context.governed_context || []).map((row: any) => ({
        ...row, label: row.statement, type: "claim", state: "admitted",
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
        description: "Summarize the signed-in workspace, review queue, and current governed context without changing state.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: {} },
        execute: async () => {
          const [graph, context, summary] = await Promise.all([api("/owner/api/graph"), api("/owner/api/context"), api("/owner/api/summary")]);
          const claims = (graph.nodes || []).filter((node: any) => node.type === "claim");
          return toolText({
            review: summary,
            current_governed_context_count: (context.governed_context || []).length,
            claim_states: claims.reduce((counts: Record<string, number>, row: any) => { counts[row.state] = (counts[row.state] || 0) + 1; return counts; }, {}),
            authority: "Agents may inspect and prepare work. Human Approval is not exposed.",
          });
        },
      },
      {
        name: "list_review_queue",
        description: "List candidate claims by review state and optional scope. This is a read-only queue view.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: { state: { type: "string", enum: ["needs_review", "needs_revision", "admitted", "rejected", "all"] }, scope: { type: "string" }, limit: { type: "integer", minimum: 1, maximum: 100 } } },
        execute: async ({ state = "needs_review", scope = "", limit = 25 }: any) => {
          const graph = await api(`/owner/api/graph?scope=${encodeURIComponent(scope)}`);
          const claims = (graph.nodes || []).filter((node: any) => node.type === "claim" && (state === "all" || node.state === state)).slice(0, limit).map((node: any) => ({ id: node.id, title: claimDisplayTitle(node), claim_title: node.title || null, statement: node.label, applicability: node.applicability || null, state: node.state, scope: node.scope, created_at: node.created_at, proposer: node.proposer }));
          return toolText({ claims, count: claims.length, open_in_review: `${location.origin}/review` });
        },
      },
      {
        name: "get_current_context",
        description:
          "Retrieve eligible governed claims for a scope. Does not approve claims.",
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
          properties: { claim_id: { type: "string" } },
          required: ["claim_id"],
        },
        execute: async ({ claim_id }: any) =>
          toolText(
            await api(
              `/owner/api/claims/${encodeURIComponent(claim_id)}`,
            ),
          ),
      },
      {
        name: "get_lineage",
        description:
          "Inspect the evidence and decision history bound to a claim.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: {
          type: "object",
          properties: { claim_id: { type: "string" } },
          required: ["claim_id"],
        },
        execute: async ({ claim_id }: any) => {
          const r = await api(
            `/owner/api/claims/${encodeURIComponent(claim_id)}`,
          );
          return toolText({
            claim: r.claim,
            state: r.state,
            evidence: r.evidence,
            history: r.history,
          });
        },
      },
      {
        name: "run_deterministic_checks",
        description: "Run deterministic integrity and policy-prerequisite checks for one candidate. This appends evaluation receipts but cannot approve claims.",
        annotations: { readOnlyHint: false, untrustedContentHint: true },
        inputSchema: { type: "object", properties: { claim_id: { type: "string" } }, required: ["claim_id"] },
        execute: async ({ claim_id }: any) => {
          await api("/owner/api/evaluate", { method: "POST", body: JSON.stringify({ csrf: csrfRef.current, claim_id }) });
          const result = await api(`/owner/api/claims/${encodeURIComponent(claim_id)}`);
          setReloadVersion(version => version + 1);
          return toolText({ claim_id, evaluation: result.evaluation, human_approval_recorded: false, next: result.review_policy?.require_judge ? "LM advice is required by policy before Human Approval." : "Open the review surface for the owner decision." });
        },
      },
      {
        name: "open_review",
        description: "Open a claim in the owner review surface. Navigation does not make a decision.",
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        inputSchema: { type: "object", properties: { claim_id: { type: "string" }, full: { type: "boolean" } }, required: ["claim_id"] },
        execute: async ({ claim_id, full = true }: any) => {
          setSelected(claim_id); setPage("review"); setFullReview(Boolean(full));
          return toolText({ opened: true, decision_recorded: false, url: `${location.origin}/review?claim_id=${encodeURIComponent(claim_id)}${full ? "&view=full" : ""}` });
        },
      },
      {
        name: "prepare_review_response",
        description:
          "Prepare instructions for an agent to answer a clarification request through its agent credential. This owner-page tool does not submit or approve.",
        inputSchema: {
          type: "object",
          properties: {
            claim_id: { type: "string" },
            response: { type: "string" },
          },
          required: ["claim_id", "response"],
        },
        execute: async ({ claim_id, response }: any) =>
          toolText({
            claim_id,
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
          "Read semantic workspace activity and claim-consumption receipts. Does not return provider secrets or owner credentials.",
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
      `/${page}${page === "review" && selected ? `?claim_id=${encodeURIComponent(selected)}${fullReview ? "&view=full" : ""}` : ""}`,
    );
  }, [page, selected, fullReview]);
  function openFullReview() {
    if (fullReview) { document.querySelector(".stage")?.scrollTo({top: 0}); return; }
    reviewScroll.current = document.querySelector(".stage")?.scrollTop || 0;
    history.pushState({proofpressFullReview: true}, "", `/review?claim_id=${encodeURIComponent(selected || "")}&view=full`);
    setFullReview(true);
  }
  function backToReview() {
    if (history.state?.proofpressFullReview) { history.back(); return; }
    history.pushState(null, "", `/review?claim_id=${encodeURIComponent(selected || "")}`);
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
      const id = new URLSearchParams(location.search).get("claim_id");
      if (id) void choose(id);
      else { ++selectionRequest.current; setSelected(null); setReceipt(null); setDetailError(""); }
    };
    window.addEventListener("popstate", restore);
    return () => window.removeEventListener("popstate", restore);
  }, []);
  async function choose(id: string) {
    if (decisionPending.current) return;
    if (selected === id && receipt?.claim.id === id) return;
    const request = ++selectionRequest.current;
    setSelected(id);
    setReceipt(null);
    setNote("");
    setError("");
    setDetailError("");
    try {
      const detail = await api(`/owner/api/claims/${encodeURIComponent(id)}`);
      if (request === selectionRequest.current) setReceipt(detail);
    } catch (e: any) {
      if (request === selectionRequest.current) {
        setDetailError(e.message);
        if (page !== "review") setError(e.message);
      }
    }
  }
  async function decide(decision: string, confirmed = false) {
    if (decisionPending.current || !receipt || receipt.claim.id !== selected) return;
    if (pendingRejection) {
      setError("Finish or undo the pending rejection before making another decision.");
      return;
    }
    if (["reject", "request_changes"].includes(decision) && !note.trim()) {
      setError(decision === "reject" ? "Explain why the evidence does not support this claim." : "Describe the bounded change the proposer should make.");
      return;
    }
    if (["admit", "reject"].includes(decision) && !confirmed) {
      decisionTrigger.current = document.activeElement as HTMLElement;
      setError("");
      setDecisionConfirmation({decision, id: receipt.claim.id, statement: receipt.claim.statement, scope: reuseBoundary(receipt.claim)});
      return;
    }
    if (decision === "reject") {
      const rejectedId = receipt.claim.id;
      const rejectionNote = note.trim();
      const nextPending = rows.find(row => row.state === "needs_review" && row.id !== rejectedId)?.id || null;
      setDecisionConfirmation(null);
      setNote("");
      setFullReview(false);
      setPendingRejection({id: rejectedId, note: rejectionNote, nextId: nextPending, seconds: 10});
      if (nextPending) void choose(nextPending);
      else { setSelected(null); setReceipt(null); }
      requestAnimationFrame(() => document.querySelector(".reviewWorkspace > .work")?.scrollTo({top: 0, behavior: "smooth"}));
      rejectCountdown.current = window.setInterval(() => {
        setPendingRejection(current => current ? {...current, seconds: Math.max(0, current.seconds - 1)} : null);
      }, 1000);
      rejectTimeout.current = window.setTimeout(async () => {
        if (rejectCountdown.current !== null) window.clearInterval(rejectCountdown.current);
        rejectCountdown.current = null;
        rejectTimeout.current = null;
        decisionPending.current = true;
        setBusy(true);
        try {
          await api("/owner/api/reviews", {
            method: "POST",
            body: JSON.stringify({csrf, claim_id: rejectedId, decision: "reject", note: rejectionNote}),
          });
          setPendingRejection(null);
          await load(nextPending);
        } catch (e: any) {
          setPendingRejection(null);
          setError(`Rejection was not recorded: ${e.message}`);
          setFullReview(true);
          setSelected(rejectedId);
          try { setReceipt(await api(`/owner/api/claims/${encodeURIComponent(rejectedId)}`)); }
          catch (detail: any) { setDetailError(detail.message); }
        } finally {
          decisionPending.current = false;
          setBusy(false);
        }
      }, 10000);
      return;
    }
    decisionPending.current = true;
    setBusy(true);
    try {
      const nextPending = decision === "admit"
        ? rows.find(row => row.state === "needs_review" && row.id !== selected)?.id || null
        : null;
      const next = await api("/owner/api/reviews", {
        method: "POST",
        body: JSON.stringify({ csrf, claim_id: selected, decision, note }),
      });
      setDecisionConfirmation(null);
      setNote("");
      if (decision === "admit") {
        setFullReview(false);
        await load(nextPending);
        requestAnimationFrame(() => document.querySelector(".stage")?.scrollTo({top: 0, behavior: "smooth"}));
      } else {
        setReceipt(next);
        await load();
        if (decision === "request_changes") setRevisionHandoff(next);
      }
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
    setJudgeRunning(true);
    setError("");
    setJudgeMessage("Reviewing bound evidence… You can keep reading this claim.");
    try {
      await api("/owner/api/judge", {method: "POST", body: JSON.stringify({csrf, claim_id: receipt.claim.id, confirmed: true})});
      const next = await api(`/owner/api/claims/${encodeURIComponent(receipt.claim.id)}`);
      setReceipt(next);
      setJudgeMessage("LM advice recorded. See Checks for the reasoning.");
    } catch { setJudgeMessage("LM review did not complete. You can retry; no approval was recorded."); }
    finally { decisionPending.current = false; setBusy(false); setJudgeRunning(false); }
  }
  async function runChecks() {
    if (!receipt || decisionPending.current) return;
    decisionPending.current = true; setBusy(true); setError("");
    try {
      await api("/owner/api/evaluate", {method:"POST",body:JSON.stringify({csrf,claim_id:receipt.claim.id})});
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
  const pending = rows.filter((r) => r.state === "needs_review" && r.id !== pendingRejection?.id).length;
  const admitted = contextLoading ? "…" : eligible.length;
  return (
    <div className="shell" aria-busy={busy || loading}>
      <Dialog.Root open={Boolean(decisionConfirmation)} onOpenChange={open => { if (!open && !decisionPending.current) setDecisionConfirmation(null); }}>
          <ModalSurface onOpenAutoFocus={event => { event.preventDefault(); cancelDecision.current?.focus(); }} onCloseAutoFocus={event => { event.preventDefault(); if (decisionTrigger.current?.isConnected) decisionTrigger.current.focus(); }} onPointerDownOutside={event => event.preventDefault()} onEscapeKeyDown={event => { if (decisionPending.current) event.preventDefault(); }}>
            <Dialog.Title>{decisionConfirmation?.decision === "admit" ? "Approve this claim?" : "Reject this claim?"}</Dialog.Title>
            <Dialog.Description>{decisionConfirmation?.decision === "admit" ? "Eligible agents may rely on this claim where its applicability card fits. You are making the human approval decision." : "This decision will be recorded. The claim will remain excluded from governed context."}</Dialog.Description>
            <dl><dt>Applicability</dt><dd>{decisionConfirmation?.scope}</dd></dl>
            <div className="confirmationStatement">{decisionConfirmation?.statement}</div>
            {decisionConfirmation?.decision === "reject" && <dl><dt>Reason for rejection</dt><dd>{note.trim()}</dd></dl>}
            {error && <p role="alert">{error}</p>}
            <div className="confirmationActions">
              <Button ref={cancelDecision} variant="outline" disabled={busy} onClick={() => setDecisionConfirmation(null)}>Cancel</Button>
              <Button variant={decisionConfirmation?.decision === "admit" ? "approve" : "danger"} disabled={busy} onClick={() => {
                if (!decisionConfirmation) return;
                if (selected !== decisionConfirmation.id) { setError("The selected claim changed. Close this dialog and review it again."); return; }
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
        <nav aria-label="Workspace navigation">
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
          <span className="workspaceLabel"><span className="workspaceContext">{workspaceLabel} · </span>{labels[page]}</span>
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
        {pendingRejection && (
          <div className="decisionNotice" role="status" aria-live="polite">
            <span>Rejection pending · {pendingRejection.seconds}s <small>Not recorded yet</small></span>
            <button onClick={() => {
              const id = pendingRejection.id;
              if (rejectTimeout.current !== null) window.clearTimeout(rejectTimeout.current);
              if (rejectCountdown.current !== null) window.clearInterval(rejectCountdown.current);
              rejectTimeout.current = null;
              rejectCountdown.current = null;
              setPendingRejection(null);
              setPage("review");
              setFullReview(true);
              void choose(id);
            }}>Undo</button>
          </div>
        )}
        <section className="stage">
          {page === "home" && (
            <HomePage
              pending={pending}
              admitted={admitted}
              eligible={eligible}
              loading={loading}
              contextLoading={contextLoading}
              contextError={contextError}
              rows={rows.filter(row => row.id !== pendingRejection?.id)}
              onChoose={(id: string) => { navigate("review"); choose(id); }}
              onKnowledgeChoose={(id: string) => { navigate("ledger"); choose(id); }}
              onReview={() => navigate("review")}
              onLedger={() => navigate("ledger")}
              onAdmin={() => navigate("admin")}
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
              detailError={detailError}
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
              judgeRunning={judgeRunning}
              onJudge={judgeConfigured ? () => setJudgeConfirmation(true) : undefined}
              onEvaluate={runChecks}
              onConfigurePolicy={showAdmin}
              onLedger={() => navigate("ledger")}
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
          {page === "runs" && <RunsPage rows={runs} selected={selectedRun} loading={runsLoading}
            onChoose={async (id: string) => {
              setRunsLoading(true);
              try { setSelectedRun(await api(`/owner/api/runs/${encodeURIComponent(id)}`)); }
              catch (e: any) { setError(`Run could not load: ${e.message}`); }
              finally { setRunsLoading(false); }
            }} onClose={() => setSelectedRun(null)} />}
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
        <ModalSurface><Dialog.Title>Review evidence with LM</Dialog.Title><Dialog.Description>Send this claim and its bound evidence text to <strong>{receipt?.review_policy?.model || "the configured model"}</strong>. The selected provider will process this data, and provider charges may apply. The result is advice, not authorization.</Dialog.Description><div className="modalActions"><Button variant="outline" onClick={()=>setJudgeConfirmation(false)}>Cancel</Button><Button onClick={runJudge}>Run LM review</Button></div></ModalSurface>
      </Dialog.Root>
    </div>
  );
}

function PageHead({
  title,
  description,
  action,
}: {
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
function HomePage({ pending, admitted, rows, eligible, loading, contextLoading, contextError, onReview, onLedger, onAdmin, onChoose, onKnowledgeChoose }: any) {
  const queue = rows.filter((row: NodeRow) => ["needs_review", "unresolved"].includes(row.state));
  const next = queue[0];
  const recentKnowledge = [...eligible].sort((a: NodeRow, b: NodeRow) => (b.created_at || "").localeCompare(a.created_at || "")).slice(0, 4);
  return (
    <div className="pageBody workspaceHome">
      <PageHead
        title="Your knowledge workspace"
        description="Decide what enters. Find what you can rely on. Keep the evidence in reach."
      />
      <div className="homeWorkGrid">
        <section className="homeReview" aria-labelledby="home-review-title">
          <div className="sectionTitle"><h2 id="home-review-title">Needs your decision</h2><span>{loading ? "Loading…" : `${queue.length} to review`}</span></div>
          {loading ? <p role="status">Loading candidate claims…</p> : next ? <>
            <article className="nextClaim">
              <Badge state={next.state} />
              <h3>{claimDisplayTitle(next)}</h3>{hasDistinctClaimHeading(next) && <p className="claimBodyPreview">{next.label}</p>}
              <dl><dt>Proposed use</dt><dd>{next.applicability?.title || next.applicability?.description || next.scope || "Not recorded"}</dd></dl>
              <p>Inspect the evidence and usage conditions before making a decision.</p>
              <Button onClick={() => onChoose(next.id)}>Review this claim <ChevronRight /></Button>
            </article>
            {queue.length > 1 && <div className="homeQueue">{queue.slice(1, 4).map((row: NodeRow) => <button key={row.id} onClick={() => onChoose(row.id)}><span>{claimDisplayTitle(row)}</span><ChevronRight /></button>)}</div>}
            <Button variant="outline" onClick={onReview}>Open review queue{pending > 0 ? ` · ${pending} pending` : ""}<ChevronRight /></Button>
          </> : <div className="emptyState"><strong>You are caught up</strong><p>New candidate claims stay outside governed context until you review them.</p><Button variant="outline" onClick={onReview}>View review history</Button></div>}
          {rows.some((r: NodeRow) => r.state === "needs_revision") && <button className="revisionQueueLink" onClick={() => onChoose(rows.find((r: NodeRow) => r.state === "needs_revision").id)}>{rows.filter((r: NodeRow) => r.state === "needs_revision").length} awaiting agent revision <ChevronRight /></button>}
        </section>
        <section className="homeKnowledge" aria-labelledby="home-knowledge-title">
          <div className="sectionTitle"><h2 id="home-knowledge-title">Available knowledge</h2><span>{contextLoading ? "Loading…" : contextError ? "Unavailable" : `${admitted} current`}</span></div>
          <p>Admitted and eligible for this owner view. Each agent’s access is checked separately.</p>
          {contextLoading ? <p role="status">Loading current knowledge…</p> : contextError ? <p role="alert">Knowledge could not be loaded. Use Reload workspace to retry.</p> : recentKnowledge.length ? <div className="homeKnowledgeList">{recentKnowledge.map((row: NodeRow) => <button key={row.id} onClick={() => onKnowledgeChoose(row.id)}><strong>{claimDisplayTitle(row)}</strong>{hasDistinctClaimHeading(row) && <p className="claimBodyPreview">{row.label}</p>}<span>{row.applicability?.title || row.applicability?.description || row.scope || "Applicability not recorded"}</span><ChevronRight /></button>)}</div> : <div className="emptyState"><strong>No claims are available for reuse</strong><p>Approved claims appear here when they are current and eligible.</p></div>}
          <Button variant="outline" onClick={onLedger}>Browse knowledge <BookOpen /></Button>
        </section>
      </div>
      {!loading && !rows.length && <section className="homeGettingStarted"><div><h2>No claims yet</h2><p>Connect an agent to submit evidence and propose the first claim. Nothing becomes reusable without your approval.</p></div><Button variant="outline" onClick={onAdmin}>Manage agent access</Button></section>}
      <details className="homeLifecycle"><summary>How claims move through Proofpress</summary>
      <ol className="claimsPath" aria-label="How claims move through Proofpress">
        <li>
          <span>Candidate</span>
          <strong>Agents propose</strong>
          <p>Evidence and a scoped claim enter the review queue.</p>
        </li>
        <li>
          <span>Review</span>
          <strong>You decide</strong>
          <p>Inspect the evidence, checks, recommendation, and reuse boundary.</p>
        </li>
        <li>
          <span>Current claims</span>
          <strong>Approved claims become reusable</strong>
          <p>Eligibility is still checked for each scope and identity.</p>
        </li>
      </ol>
      </details>
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
  judgeRunning,
  onJudge, onEvaluate, onConfigurePolicy,
  fullReview, onOpenFull, onBack, onLedger, detailError,
}: any) {
  const [queue, setQueue] = React.useState("needs_review");
  const [reviewPage, setReviewPage] = React.useState(0);
  const pageSize = 20;
  const queueFor = (state: string) => state === "unresolved" ? "needs_review" : ["needs_review", "needs_revision"].includes(state) ? state : "decided";
  React.useEffect(() => { if (selected && receipt?.claim.id === selected) { setQueue(queueFor(receipt.state)); setReviewPage(0); } }, [selected, receipt?.state]);
  const visibleRows = rows.filter((row: any) => queueFor(row.state) === queue).sort((left: any, right: any) => {
    const leftTime = Date.parse(queue === "decided" ? left.decision_at || left.created_at || "" : left.created_at || "");
    const rightTime = Date.parse(queue === "decided" ? right.decision_at || right.created_at || "" : right.created_at || "");
    return (Number.isFinite(rightTime) ? rightTime : 0) - (Number.isFinite(leftTime) ? leftTime : 0) || right.id.localeCompare(left.id);
  });
  const pageCount = Math.max(1, Math.ceil(visibleRows.length / pageSize));
  const currentPage = Math.min(reviewPage, pageCount - 1);
  const pageRows = visibleRows.slice(currentPage * pageSize, (currentPage + 1) * pageSize);
  const switchQueue = (next: string) => { onClose(); setQueue(next); setReviewPage(0); };
  return (
    <div className={`workspacePage reviewWorkspace${selected ? "" : " overviewOnly"}${fullReview ? " fullReviewPage" : ""}`}>
      <div className="work" style={fullReview ? {display: "none"} : undefined}>
        <PageHead
          title="Review"
          description="Evidence and recommendations inform the decision. Only your approval admits claims."
        />
        <div className="filterbar">
          <Button variant={queue === "needs_review" ? "default" : "outline"} onClick={() => switchQueue("needs_review")}>Needs review</Button>
          <Button variant={queue === "needs_revision" ? "default" : "outline"} onClick={() => switchQueue("needs_revision")}>Needs revision</Button>
          <Button variant={queue === "decided" ? "default" : "outline"} onClick={() => switchQueue("decided")}>Decision history</Button>
          <span role="status">{loading ? "Loading review queue…" : `${visibleRows.length} claims`}</span>
        </div>
        <div className="tableWrap reviewTableWrap">
          <table className="reviewTable">
            <thead>
              <tr>
                <th>Claim</th>
                <th>Status</th>
                <th>Applicability</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {pageRows.map((row: any) => (
                <tr
                  key={row.id}
                  className={selected === row.id ? "selected" : ""}
                  onClick={() => onChoose(row.id)}
                >
                  <td data-label="Claim">
                    <button className="claimSelect" onClick={e => { e.stopPropagation(); onChoose(row.id); }}>{claimDisplayTitle(row)}</button>
                    <small>{row.id}<span className="claimScopeInline"><b>Applies to</b>{row.applicability?.title || row.scope || "No reuse boundary"}</span></small>
                  </td>
                  <td data-label="Status"><Badge state={row.state} /></td>
                  <td className="reviewScopeCell" data-label="Applicability">{row.applicability?.title || row.applicability?.description || row.scope || "—"}</td>
                  <td aria-label="Open claim">
                    <ChevronRight />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!loading && visibleRows.length === 0 && (
            <div className="emptyState reviewEmpty">
              <strong>{queue === "needs_review" ? "You are caught up" : queue === "needs_revision" ? "No revision requests" : "No decisions yet"}</strong>
              <p>{queue === "needs_review" ? "New candidate claims will appear here and remain excluded until you approve them." : queue === "needs_revision" ? "Requests you send to agents remain here until a revised claim is submitted." : "Your approval, rejection, and revision decisions will appear here."}</p>
              {queue === "needs_review" && <Button variant="outline" onClick={onLedger}>Browse current claims</Button>}
            </div>
          )}
        </div>
        {!loading && visibleRows.length > 0 && <nav className="pagination reviewPagination" aria-label={`${queue === "decided" ? "Decision history" : "Review queue"} pages`}>
          <Button variant="outline" disabled={currentPage === 0} onClick={() => setReviewPage(currentPage - 1)}>Previous</Button>
          <span>Page {currentPage + 1} of {pageCount} · {visibleRows.length} {queue === "decided" ? "decisions" : "claims"} · {pageSize} per page</span>
          <Button variant="outline" disabled={currentPage + 1 >= pageCount} onClick={() => setReviewPage(currentPage + 1)}>Next</Button>
        </nav>}
      </div>
      <Inspector
        pending={!!selected && !receipt}
        detailError={detailError}
        receipt={receipt && visibleRows.some((row: any) => row.id === selected) ? receipt : null}
        onClose={onClose}
        note={note}
        setNote={setNote}
        onDecide={onDecide}
        busy={busy}
        judgeRunning={judgeRunning}
        onJudge={onJudge}
        onEvaluate={onEvaluate}
        onConfigurePolicy={onConfigurePolicy}
        fullReview={fullReview}
        onOpenFull={onOpenFull}
        onBack={onBack}
        onChoose={onChoose}
      />
    </div>
  );
}
function ReviewFact({label,value,tone="",className=""}:any){
  return <Card className={`reviewFact ${className}`}><CardContent className="reviewFactContent"><span>{label}</span><strong className={tone}>{value}</strong></CardContent></Card>;
}

function ApplicabilityPanel({claim, compact = false}: {claim: Receipt["claim"]; compact?: boolean}) {
  const relevant = claim.applicability?.when_relevant || [];
  const conditions = claim.applicability?.validity_conditions || [];
  return <section className="applicabilityPanel space-y-4" aria-label="Applicability and conditions">
    <div className="space-y-1.5">
      <h3 className="font-['DM_Sans'] text-base font-semibold leading-6 text-[var(--ink)]">{reuseBoundary(claim)}</h3>
      {claim.applicability?.description && claim.applicability.description !== reuseBoundary(claim) && <p className="max-w-[65ch] font-['DM_Sans'] text-sm leading-6 text-[var(--ink-2)]">{claim.applicability.description}</p>}
    </div>
    <div className={compact ? "grid gap-3" : "grid gap-3 md:grid-cols-2"}>
      <Card className="shadow-none"><CardContent className="space-y-2 p-5">
        <h4 className="font-['DM_Sans'] text-sm font-semibold text-[var(--ink)]">Relevant when</h4>
        {relevant.length ? <ul className="space-y-2 pl-5 font-['DM_Sans'] text-sm leading-6 text-[var(--ink-2)]">{relevant.map((item, i) => <li key={i}>{item}</li>)}</ul> : <p className="font-['DM_Sans'] text-sm text-[var(--ink-2)]">Not recorded</p>}
      </CardContent></Card>
      <Card className="shadow-none"><CardContent className="space-y-2 p-5">
        <h4 className="font-['DM_Sans'] text-sm font-semibold text-[var(--ink)]">Validity conditions</h4>
        {conditions.length ? <ul className="space-y-2 pl-5 font-['DM_Sans'] text-sm leading-6 text-[var(--ink-2)]">{conditions.map((item, i) => <li key={i}>{item}</li>)}</ul> : <p className="font-['DM_Sans'] text-sm text-[var(--ink-2)]">Not recorded</p>}
      </CardContent></Card>
    </div>
  </section>;
}
function Inspector({
  receipt: r,
  onClose,
  note,
  setNote,
  onDecide,
  busy,
  judgeRunning = false,
  onJudge, onEvaluate,
  readOnly = false,
  fullReview = false, onOpenFull, onBack, onChoose, onConfigurePolicy, onViewLineage, pending = false, detailError = "",
}: any) {
  const [expanded, setExpanded] = React.useState(false);
  const panel = React.useRef<HTMLElement>(null);
  React.useEffect(() => {
    setExpanded(false);
    panel.current?.scrollTo({top: 0, behavior: "auto"});
  }, [r?.claim.id]);
  React.useEffect(() => {
    if (!r || !window.matchMedia("(max-width: 899px)").matches) return;
    const opener = document.querySelector<HTMLElement>(".work tr.selected .claimSelect") || document.activeElement as HTMLElement | null;
    panel.current?.querySelector<HTMLButtonElement>(".mobileBack")?.focus();
    return () => { requestAnimationFrame(() => { if (opener?.isConnected && opener !== document.body) opener.focus(); }); };
  }, [r?.claim.id]);
  if (!r) {
    if (detailError) return <aside className={`inspector${fullReview ? " fullReview" : ""}`} aria-label="Claim details"><div className="missingConclusion"><strong>Claim not found</strong><p>{detailError}</p><Button variant="outline" onClick={fullReview ? onBack : onClose}>Back to review queue</Button></div></aside>;
    return pending ? <aside className={`inspector${fullReview ? " fullReview" : ""}`} aria-label="Claim details" aria-busy="true"><div className="inspectorTop" role="status">Loading details…</div></aside> : null;
  }
  const can = ["needs_review", "unresolved"].includes(r.state) && !readOnly;
  const failedChecks = Object.entries(r.evaluation?.checks || {}).filter(([,passed])=>!passed).map(([key])=>key.replaceAll("_", " "));
  const checkReason = (name:string) => ({"evidence present":"Required evidence missing","evidence integrity":"Evidence integrity unverified","experiment evidence present":"Typed experiment evidence missing","experiment evidence valid":"Experiment evidence invalid","experiment identity bound":"Experiment identity unbound","not expired":"Claim expired","not superseded":"Claim superseded","reuse boundary present":"Reuse boundary missing"} as Record<string,string>)[name] || `${name} failed`;
  const checksMissing = !Object.keys(r.evaluation?.checks || {}).length || (r.review_policy && !r.review_policy.checks_current);
  const judgeNeedsSetup = r.review_policy?.mode === "off";
  const judgePending = r.review_policy?.mode !== "off" && !r.recommendation;
  const judgeInProgress = judgeRunning || (!r.recommendation && ["queued", "running"].includes(r.judge_job?.state));
  const judgeFailed = !r.recommendation && ["failed", "interrupted"].includes(r.judge_job?.state);
  const approvalBlock = !Object.keys(r.evaluation?.checks || {}).length ? "Run deterministic checks before approval." : failedChecks.length ? failedChecks.map(checkReason).join(" · ") : r.review_policy && !r.review_policy.checks_current ? "Review policy changed. Run checks again before approval." : r.review_policy?.require_judge && !r.review_policy.advice_current ? "The workspace requires current, supporting LM advice. Refresh the LM review before approval." : r.review_policy?.require_judge && r.recommendation?.recommendation === "escalate" ? "The LM marked this claim Needs Attention. This workspace requires supporting LM advice before you can approve; review the rationale, then request a bounded revision if the evidence is incomplete." : r.review_policy?.require_judge && r.recommendation?.recommendation === "reject" ? "The LM found that the evidence does not support this claim. This workspace requires supporting LM advice before you can approve; review the rationale, then reject or request a bounded revision." : r.review_policy?.require_judge && r.recommendation?.recommendation !== "accept" ? "This workspace requires supporting LM advice before approval." : "";
  const evidenceRows = r.evidence || [];
  const previewEvidence = evidenceRows.slice(0, 2);
  const claimTitle = claimDisplayTitle(r.claim);
  const claimDescription = r.claim.applicability?.description || "";
  const hasConciseHeading = hasDistinctClaimHeading(r.claim);
  const InspectorHeader: any = fullReview ? Card : "div";
  return (
    <aside className={`inspector${fullReview ? " fullReview" : ""}`} ref={panel} aria-label="Claim details" onKeyDown={e => { if (e.key === "Escape" && onClose) { e.stopPropagation(); fullReview ? onBack() : onClose(); } }}>
      {!can && !readOnly && <DecisionNotice state={r.state}>{r.state === "blocked" && <p>Deterministic requirements did not pass. This candidate is excluded from LM and human review.</p>}</DecisionNotice>}
      {fullReview && <Button className="fullReviewBack" variant="ghost" onClick={onBack}>Back to review</Button>}
      {!fullReview && onClose && <button className="mobileBack" onClick={onClose}>
        Close details
      </button>}
      <InspectorHeader className="inspectorTop">
        {(can || readOnly || !fullReview) && <Badge state={r.state} />}
        {r.state === "unresolved" && <p>Previous approval needs revalidation under the current policy.</p>}
        {fullReview ? <h1 className="fullStatement">{claimTitle}</h1> : <h2>{claimTitle}</h2>}
        {claimDescription && <p className="claimDescription">{claimDescription}</p>}
        {hasConciseHeading && <details className="claimStatementDetails"><summary>Exact claim statement</summary><p className="claimFullStatement">{r.claim.statement}</p></details>}
        <p>
          Proposed by {r.claim.proposer || "Not recorded"} ·{" "}
          <span className="mono">{r.claim.id}</span>
        </p>
        {onOpenFull && !fullReview && (can ? <Button className="reviewEntry" variant="accent" onClick={onOpenFull}>Open full review</Button> : <Button className="reviewEntry" variant="accent" onClick={onOpenFull}>{r.state === "needs_revision" ? "View revision request" : "View decision"}</Button>)}
      </InspectorHeader>
      {r.revision_request && <RevisionPanel receipt={r} onChoose={onChoose} />}
      <div className="quickSnapshot">
        {fullReview ? <div className="reviewFactsGrid">
          <ReviewFact label="Applies to" value={reuseBoundary(r.claim)} />
          <ReviewFact label="Supporting evidence" value={`${evidenceRows.length} bound ${evidenceRows.length === 1 ? "source" : "sources"}`} />
          {can && <><ReviewFact label="Deterministic checks" value={checksMissing ? (r.evaluation ? "Recheck required" : "Not run") : failedChecks.length ? `${failedChecks.length} requirements failed` : "Passed"} tone={!checksMissing && !failedChecks.length ? "pass" : ""} /><ReviewFact label="LM advice · advisory" value={r.recommendation ? (r.review_policy && !r.review_policy.advice_current ? "Refresh required" : r.recommendation.recommendation === "accept" ? "Supports the evidence" : r.recommendation.recommendation) : "Not recorded"} /><ReviewFact className="authorityFact" label="Owner authorization" value={approvalBlock ? "Unavailable until requirements pass" : "Ready for your decision"} /></>}
        </div> : <dl><div><dt>Applies to</dt><dd>{reuseBoundary(r.claim)}</dd></div>
        <div><dt>Supporting evidence</dt><dd>{(r.evidence || []).length} bound {(r.evidence || []).length === 1 ? "source" : "sources"}</dd></div>
        {!fullReview && !can && <><div><dt>Automated checks</dt><dd className={r.evaluation ? (failedChecks.length ? "checkSummary fail" : "checkSummary pass") : ""}>{Object.keys(r.evaluation?.checks || {}).length ? `${Object.values(r.evaluation.checks).filter(Boolean).length} of ${Object.keys(r.evaluation.checks).length} passed` : "Not run"}</dd></div>
        <div><dt>LM advice</dt><dd>{r.recommendation ? <Badge state={r.recommendation.recommendation} /> : judgeInProgress ? "Review in progress" : judgeFailed ? "Review failed" : judgeNeedsSetup || !onJudge ? "Policy setup required" : "Not run yet"}</dd></div></>}</dl>}
        {judgeInProgress && <div className="lmReviewProgress" role="status" aria-live="polite"><span className="lmSpinner" aria-hidden="true" /><div><strong>LM is reviewing the bound evidence</strong><p>Checking whether each source supports the exact claim and reuse boundary.</p></div></div>}
        {can && !fullReview && <dl className="decisionStack"><div><dt>Deterministic checks</dt><dd className={checksMissing ? "" : failedChecks.length ? "fail" : "pass"}>{checksMissing ? (r.evaluation ? "Recheck required" : "Not run") : failedChecks.length ? `Blocking · ${failedChecks.length} requirement${failedChecks.length===1?"":"s"} failed` : "Passed"}</dd></div><div><dt>LM advice · advisory</dt><dd>{r.recommendation ? (r.review_policy && !r.review_policy.advice_current ? "Refresh required · previous advice recorded" : r.recommendation.recommendation === "accept" ? "Supports the evidence" : r.recommendation.recommendation) : "Not recorded"}</dd></div><div className="authorityStep"><dt>Owner authorization</dt><dd>{approvalBlock ? "Unavailable until requirements pass" : "Ready for your decision"}</dd></div></dl>}
        {can && approvalBlock && <p className="approvalBlock" role="status">{approvalBlock}</p>}
        {r.judge_job && ((judgeFailed && ["failed","interrupted"].includes(r.judge_job.state)) || r.judge_job.state === "blocked") && <p>{r.judge_job.detail}</p>}
        {can && (checksMissing || !failedChecks.length) && <div className="reviewActions">
          {checksMissing && onEvaluate ? <Button disabled={busy} onClick={onEvaluate}>Run deterministic checks</Button>
            : <>
              {(judgeNeedsSetup || !onJudge) && onConfigurePolicy
                ? <Button variant="outline" onClick={onConfigurePolicy}>Set up LM review</Button>
                : judgeFailed && onJudge
                  ? <Button variant="outline" disabled={busy} onClick={onJudge}>Retry LM review</Button>
                  : judgePending && r.review_policy?.mode === "automatic"
                    ? <span className="queuedAction">LM review runs automatically after checks</span>
                    : judgePending && onJudge && r.review_policy?.mode === "manual"
                      ? <Button variant="outline" disabled={busy} onClick={onJudge}>Run optional LM review</Button>
                      : null}
            </>}
          {r.recommendation && onJudge && <Button className="secondaryAction" variant="ghost" disabled={busy} onClick={onJudge}>Refresh LM advice</Button>}
          {approvalBlock && r.review_policy?.require_judge && onConfigurePolicy && <Button className="secondaryAction" variant="ghost" disabled={busy} onClick={onConfigurePolicy}>Review approval policy</Button>}
        </div>}
        {can && !fullReview && <section className="evidenceArgument" aria-labelledby="evidence-argument-title">
          <div className="evidenceArgumentHead">
            <h3 id="evidence-argument-title">Evidence for this claim</h3>
            <span>{previewEvidence.length < evidenceRows.length ? `${previewEvidence.length} of ${evidenceRows.length} sources` : `${evidenceRows.length} ${evidenceRows.length === 1 ? "source" : "sources"}`}</span>
          </div>
          {evidenceRows.length ? <div className="evidenceArgumentList">{previewEvidence.map((e: any, i: number) => <article key={e.id || i}>
            <strong title={evidenceName(e)}>{evidenceName(e)}</strong>
            <EvidencePreview row={e} />
          </article>)}</div> : <p className="evidenceArgumentEmpty">No evidence is bound. This claim cannot be approved.</p>}
        </section>}
        {can && (fullReview ? <Accordion type="single" collapsible className="reviewDisclosure"><AccordionItem value="applicability"><AccordionTrigger>Applicability & conditions</AccordionTrigger><AccordionContent className="pt-2"><ApplicabilityPanel claim={r.claim} /></AccordionContent></AccordionItem></Accordion> : <Card className="m-5 shadow-none"><CardContent className="p-5"><ApplicabilityPanel claim={r.claim} compact /></CardContent></Card>)}
        {r.recommendation?.rationale && (fullReview ? <Accordion type="single" collapsible className="reviewDisclosure"><AccordionItem value="rationale"><AccordionTrigger><span className="accordionLabel">LM rationale <Badge state={r.recommendation.recommendation} /></span></AccordionTrigger><AccordionContent><p>{r.recommendation.rationale}</p><small>The LM evaluates evidence support. Only Human Approval admits the claim.</small></AccordionContent></AccordionItem></Accordion> : <section className="lmRationale" aria-label="LM review rationale"><div className="lmRationaleHeader"><span>Why the LM reached this advice</span><Badge state={r.recommendation.recommendation} /></div><ExpandableText key={r.claim.id} text={r.recommendation.rationale} label="Read full LM rationale" /><small>The LM evaluates evidence support. Only Human Approval admits the claim.</small></section>)}
        {!can && !onOpenFull && <Button variant="outline" aria-expanded={expanded} onClick={() => setExpanded(!expanded)}>{expanded ? "Hide details" : "View details"}</Button>}
        {readOnly && onViewLineage && <Button className="viewLineageAction" variant="outline" onClick={onViewLineage}>View lineage</Button>}
      </div>
      {(fullReview || expanded) && <>
      {r.revision_parent && <section className="revisionSection"><h3>Revision of previous claim</h3><p>{r.revision_parent.statement}</p><p><b>Requested change:</b> {r.revision_parent.review?.note}</p><p>Previous evidence: {r.revision_parent.evidence_refs.join(", ")}</p><p>Current evidence: {r.claim.evidence_refs.join(", ")}</p><p>This proposal requires a new human decision; it does not automatically replace its predecessor.</p></section>}
      {r.reproposal_parent && <details className="revisionDisclosure"><summary><span>Re-proposal context</span><small>Previous rejection, response, and evidence changes</small></summary><div className="revisionSection"><h3>Previous rejection</h3><p>{r.reproposal_parent.rejection_reason || r.reproposal_parent.review?.note || "No rejection reason was recorded."}</p><h3>Response to the rejection</h3><p>{r.reproposal_parent.reproposal_response || "No response was recorded for this legacy re-proposal."}</p><dl><div><dt>New evidence</dt><dd>{r.reproposal_parent.new_evidence_refs?.length ? r.reproposal_parent.new_evidence_refs.join(", ") : "None"}</dd></div><div><dt>Reused evidence</dt><dd>{r.reproposal_parent.reused_evidence_refs?.length ? r.reproposal_parent.reused_evidence_refs.join(", ") : "None"}</dd></div></dl><small>The earlier rejection remains in the append-only history. This candidate requires a new human decision.</small></div></details>}
      {!!r.reproposals?.length && <section className="revisionSection"><h3>Re-proposals after this rejection</h3><p>These are separate candidates. The rejection above remains part of the append-only history.</p>{r.reproposals.map((candidate:any) => <Button key={candidate.id} variant="outline" onClick={() => onChoose?.(candidate.id)}>{candidate.statement} · {candidate.state.replaceAll("_", " ")}</Button>)}</section>}
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
              <EvidenceContent row={e} collapsible={fullReview} />
              <small>Bound to this claim</small>
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
            {r.recommendation && <p>Read the complete advisory rationale in the review summary above.</p>}
          </div>
        </Tabs.Content>
        <Tabs.Content value="history" className="tabContent">
          {(r.history || []).map((h: any, i: number) => (
            <div className="historyRow" key={i}>
              <span></span>
              <div>
                <b>{h.type.replaceAll("_", " ")}</b>
                <p>{historyActor({...([r.evaluation, r.recommendation, r.review, r.admission, r.rejection].find(event => event?.event_id === h.event_id) || {}), ...(h.type === "claim_proposed" ? {claim:r.claim} : {}), ...h})}</p>
                {h.note && <p>{h.note}</p>}
                <small>{h.created_at}</small>
              </div>
            </div>
          ))}
        </Tabs.Content>
      </Tabs.Root>
      </>}
      {can && (!onOpenFull || fullReview) ? (
        <Card className="decision">
          <div className="decisionHeading">
            <span>Owner decision</span>
            <p>Approve for eligible reuse, reject the claim, or request a bounded revision.</p>
          </div>
          <label htmlFor={`decision-note-${r.claim.id}`}>Decision note <small>Required for reject or request changes</small></label>
          <Textarea
            id={`decision-note-${r.claim.id}`}
            aria-label="Reason for rejection or bounded clarification request"
            aria-required="true"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Explain why the evidence does not support this claim, or describe a bounded change."
          />
          <small className="decisionHint">A reason is required for Reject and Request changes, so a future re-proposal can address it.</small>
          <div>
            <Button
              variant="danger"
              disabled={busy}
              onClick={() => onDecide("reject")}
            >
              Reject
            </Button>
            <Button
              variant="request"
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
              Approve
            </Button>
          </div>
        </Card>
      ) : null}
    </aside>
  );
}
function LedgerPage(props: any) {
  return <KnowledgeLibrary {...props} evidenceName={evidenceName} renderEvidence={(row: any) => <EvidenceContent row={row} />} />;
}
function RunsPage({ rows, selected, loading, onChoose, onClose }: any) {
  const when = (value?: string) => value ? new Date(value).toLocaleString() : "—";
  return <div className="pageBody runsPage">
    <PageHead title="Runs" description="Trace each task from retrieved knowledge through declared reliance, outputs, and observed results." />
    <div className={`runsWorkspace${selected ? " hasRun" : ""}`}>
      <section className="runList" aria-busy={loading}>
        {rows.map((run: any) => <button key={run.id} className={selected?.id === run.id ? "active" : ""} onClick={() => onChoose(run.id)}>
          <span><Badge state={run.status} /><time>{when(run.started_at)}</time></span>
          <strong>{run.purpose}</strong>
          <small>{run.actor} · {run.counts?.retrieved || 0} receipts · {run.counts?.outputs || 0} outputs</small>
        </button>)}
        {!loading && !rows.length && <div className="empty"><h2>No runs recorded</h2><p>Agent-tracked tasks appear here after run.start.</p></div>}
      </section>
      {selected && <article className="runDetail">
        <header><div><Badge state={selected.status} /><h2>{selected.purpose}</h2><p>{selected.actor} · started {when(selected.started_at)}{selected.finished_at ? ` · finished ${when(selected.finished_at)}` : ""}</p></div><Button variant="outline" onClick={onClose}>Close</Button></header>
        {selected.finish_summary && <p className="runSummary">{selected.finish_summary}</p>}
        <section><h3>Retrieved context</h3>{selected.context_receipts?.length ? selected.context_receipts.map((receipt: any) => <div className="runRecord" key={receipt.id}><b>{receipt.claims.length} claim versions</b><small className="mono">{receipt.id}</small>{receipt.claims.map((claim: any) => <details key={`${claim.claim_id}:${claim.claim_digest}`}><summary>{claim.title || claim.statement}</summary><p>{claim.statement}</p><code>{claim.claim_id} · {claim.claim_digest}</code></details>)}<details className="technicalDetails"><summary>Technical receipt</summary><code>Ledger {receipt.ledger_head || "empty"}</code><code>Policy {receipt.policy_digest}</code></details></div>) : <p className="empty">No context receipts recorded.</p>}</section>
        <section><h3>Declared reliance</h3>{selected.reliances?.length ? selected.reliances.map((row: any) => <div className="runRecord" key={row.id}><b>{row.purpose}</b><code>{row.claim_id} · {row.claim_digest}</code></div>) : <p className="empty">No reliance declared. Retrieved context is not treated as used.</p>}</section>
        <section><h3>Outputs</h3>{selected.outputs?.length ? selected.outputs.map((row: any) => <div className="runRecord" key={row.id}><b>{row.summary || "Output reference"}</b><code>{row.reference}</code><code>{row.content_digest}</code>{row.reliance_ids?.length ? <small>{row.reliance_ids.length} declared reliance link(s)</small> : null}</div>) : <p className="empty">No outputs recorded.</p>}</section>
        <section><h3>Observations</h3>{selected.observations?.length ? selected.observations.map((row: any) => <div className="runRecord" key={row.id}><span><Badge state={row.kind} /><time>{when(row.observed_at)}</time></span><b>{row.meaning}</b><small>Source: {row.source}</small></div>) : <p className="empty">No observations recorded. Proofpress does not infer a score.</p>}</section>
      </article>}
    </div>
  </div>;
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
        title="Activity"
        description="Who contributed claims, reviewed it, and retrieved context. Technical requests are kept separately."
      />
      <div className="ledgerViews activityFilters" role="group" aria-label="Activity filter">
        {[["activity","Claims activity"],["retrievals","Context retrievals"],["logs","Technical logs"]].map(([key,label])=><Button key={key} aria-pressed={view===key} onClick={()=>{setView(key);setPage(0);setError("");}}>{label}</Button>)}
      </div>
      {error && <p role="alert">{error}</p>}
      <div className="tableWrap activityTable">
        <table><caption className="sr-only">Recent workspace activity</caption><thead><tr><th>Time</th><th>{view==="logs"?"Operation":"What happened"}</th><th>Actor</th><th>Result</th></tr></thead><tbody>
        {filtered.slice(current * 20, (current + 1) * 20).map((r: any) => (
          <tr key={r.id || r.audit_id}>
            <td data-label="Time"><time dateTime={r.occurred_at} title={r.occurred_at}>{new Date(r.occurred_at).toLocaleString()}</time></td>
            <td data-label="What happened">{view==="logs" ? (r.operation || "request").replaceAll(".", " · ") : <><strong>{r.action}</strong>{r.statement && <a className="activitySubject" href={`/review?claim_id=${encodeURIComponent(r.subject_id)}&view=full`}>{r.statement}</a>}{r.detail && <details><summary>Details</summary><p>{r.detail}</p></details>}{r.scope && <small>{r.scope}</small>}</>}</td>
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
        title="Admin"
        description="Configure review policy and manage agent access."
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
        <div className="issueFormHeader">
          <b>Issue agent credential</b>
          <small>
            Create a key for an agent or device. You can revoke its access later.
          </small>
        </div>
        <div className="issueFormFields">
          <label>Agent identity<Input
            aria-label="Agent identity"
            aria-describedby="agentIdentityHelp"
            value={principal}
            onChange={(e) => setPrincipal(e.target.value)}
            placeholder="agent:claude-code"
            required
          /><small id="agentIdentityHelp">Recorded as the author in history, e.g. agent:claude-code.</small></label>
          <label>Key name<Input
            aria-label="Key name"
            aria-describedby="keyNameHelp"
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            placeholder="Claude Code · company laptop"
            required
          /><small id="keyNameHelp">A name you recognize, such as Claude Code · work laptop.</small></label>
          <Button disabled={busy}>Issue credential</Button>
        </div>
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
                  size="sm"
                  disabled={busy}
                  onClick={() =>
                    onAction("rotate", { credential_id: c.credential_id })
                  }
                >
                  Rotate
                </Button>
                <Button
                  variant="danger"
                  size="sm"
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
            Agent credentials can submit evidence, propose claims, and read
            admitted context. They cannot approve claims or change policy.
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
