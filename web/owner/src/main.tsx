import React from "react";
import { createRoot } from "react-dom/client";
import ReactMarkdown from "react-markdown";
import * as Dialog from "@radix-ui/react-dialog";
import * as Tabs from "@radix-ui/react-tabs";
import {
  Activity,
  Bot,
  BookOpen,
  Check,
  ChevronRight,
  CircleUserRound,
  Home,
  KeyRound,
  MessageSquareText,
  PanelRightClose,
  Search,
  ShieldCheck,
  X,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import "./index.css";

type NodeRow = {
  id: string;
  type: string;
  label: string;
  state: string;
  scope?: string;
};
type Receipt = {
  state: string;
  conclusion: {
    id: string;
    statement: string;
    scope?: string;
    proposer?: string;
  };
  evidence?: any[];
  evaluation?: { checks?: Record<string, boolean> };
  recommendation?: { recommendation?: string; rationale?: string };
  history?: any[];
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
  const body = await response.json();
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
  return row?.source?.uri || row?.path || row?.kind || "Bound evidence";
}
function evidenceText(row: any) {
  const p = row?.experiment_profile || {};
  if (p.cell) return `${p.cell.value} ${p.cell.unit || ""}`;
  if (p.observation)
    return `${p.observation.value} ${p.observation.unit || ""}`;
  if (p.derivation)
    return `${p.derivation.formula?.operation || "recompute"} → ${p.derivation.output?.value}`;
  return row?.quote || row?.source_ref || "Digest-verified evidence";
}

function App() {
  const path = (location.pathname.split("/")[1] || "review") as Page;
  const [page, setPage] = React.useState<Page>(labels[path] ? path : "review");
  const [rows, setRows] = React.useState<NodeRow[]>([]);
  const [selected, setSelected] = React.useState<string | null>(
    new URLSearchParams(location.search).get("conclusion_id"),
  );
  const [receipt, setReceipt] = React.useState<Receipt | null>(null);
  const [query, setQuery] = React.useState("");
  const [scope, setScope] = React.useState("");
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState("");
  const [csrf, setCsrf] = React.useState("");
  const [assistant, setAssistant] = React.useState(false);
  const [question, setQuestion] = React.useState("");
  const [messages, setMessages] = React.useState<
    { role: string; text: string }[]
  >([]);
  const [note, setNote] = React.useState("");
  const [busy, setBusy] = React.useState(false);
  const [credentials, setCredentials] = React.useState<any[]>([]);
  const [activity, setActivity] = React.useState<any[]>([]);
  const [credentialSecret, setCredentialSecret] = React.useState("");
  const load = React.useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [graph, session, audit] = await Promise.all([
        api("/owner/api/graph"),
        api("/owner/api/session"),
        api("/owner/api/activity"),
      ]);
      const next = (graph.nodes || []).filter(
        (n: NodeRow) => n.type === "conclusion",
      );
      setRows(next);
      setCsrf(session.csrf);
      setActivity(audit);
      const desired =
        selected && next.some((n: NodeRow) => n.id === selected)
          ? selected
          : next.find((n: NodeRow) => n.state === "needs_review")?.id ||
            next[0]?.id ||
            null;
      setSelected(desired);
      if (desired)
        setReceipt(
          await api(`/owner/api/conclusions/${encodeURIComponent(desired)}`),
        );
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [selected]);
  React.useEffect(() => {
    load();
  }, []);
  React.useEffect(() => {
    const ctx =
      (document as any).modelContext || (navigator as any).modelContext;
    if (!ctx?.registerTool) return;
    const toolText = (value: unknown) => ({
      content: [{ type: "text", text: JSON.stringify(value, null, 2) }],
    });
    const tools = [
      {
        name: "get_current_context",
        description:
          "Retrieve eligible governed conclusions for a scope. Does not approve knowledge.",
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
        name: "respond_to_review",
        description:
          "Prepare an agent response to a clarification request. Approve is not exposed.",
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
            recorded: false,
            admitted: false,
            next: "human review required",
          }),
      },
    ];
    Promise.all(tools.map((tool) => ctx.registerTool(tool))).catch(
      () => undefined,
    );
  }, []);
  React.useEffect(() => {
    history.replaceState(
      null,
      "",
      `/${page}${page === "review" && selected ? `?conclusion_id=${encodeURIComponent(selected)}` : ""}`,
    );
  }, [page, selected]);
  async function choose(id: string) {
    setSelected(id);
    setReceipt(await api(`/owner/api/conclusions/${encodeURIComponent(id)}`));
  }
  async function decide(decision: string) {
    if (decision === "request_changes" && !note.trim()) {
      setError("Describe the bounded change the proposer should make.");
      return;
    }
    setBusy(true);
    try {
      const next = await api("/owner/api/reviews", {
        method: "POST",
        body: JSON.stringify({ csrf, conclusion_id: selected, decision, note }),
      });
      setReceipt(next);
      setNote("");
      await load();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  async function ask() {
    if (!question.trim()) return;
    const q = question.trim();
    setMessages((m) => [...m, { role: "user", text: q }]);
    setQuestion("");
    try {
      const result = await api("/owner/api/ask", {
        method: "POST",
        body: JSON.stringify({
          csrf,
          question: q,
          snapshot: {
            page,
            scope,
            selected: receipt,
            candidates: rows.slice(0, 30).map((row) => ({
              id: row.id,
              statement: row.label,
              state: row.state,
              scope: row.scope,
            })),
            counts: {
              needs_review: rows.filter((r) => r.state === "needs_review")
                .length,
              admitted: rows.filter((r) => r.state === "admitted").length,
            },
          },
        }),
      });
      setMessages((m) => [
        ...m,
        { role: "assistant", text: result.answer || "No answer returned." },
      ]);
    } catch (e: any) {
      setMessages((m) => [...m, { role: "assistant", text: e.message }]);
    }
  }
  async function showAdmin() {
    setPage("admin");
    try {
      const body = await fetch("/v1/owner/credentials", {
        credentials: "same-origin",
      }).then((r) => r.json());
      setCredentials(body.credentials || []);
    } catch {
      setCredentials([]);
    }
  }
  async function credentialAction(
    action: string,
    values: Record<string, string>,
  ) {
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
  const filtered = rows.filter(
    (r) =>
      (!scope || r.scope?.toLowerCase().includes(scope.toLowerCase())) &&
      (!query ||
        `${r.label} ${r.id}`.toLowerCase().includes(query.toLowerCase())),
  );
  const pending = rows.filter((r) => r.state === "needs_review").length;
  const admitted = rows.filter((r) => r.state === "admitted").length;
  return (
    <div className="shell">
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
                className={page === id ? "active" : ""}
                onClick={() => (id === "admin" ? showAdmin() : setPage(id))}
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
          <b>Proofpress internal</b>
          <small>Single-owner governance</small>
        </div>
      </aside>
      <main>
        <header className="topbar">
          <div className="mobileBrand">
            <span className="brandMark"><img src="/logo.svg" alt="" /></span>
            <strong>Proofpress</strong>
          </div>
          <label className="search">
            <Search />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search conclusions, evidence, or IDs…"
            />
            <kbd>⌘ K</kbd>
          </label>
          <button
            className="iconButton"
            aria-label="Open Ask Proofpress"
            onClick={() => setAssistant(true)}
          >
            <MessageSquareText />
          </button>
          <CircleUserRound className="userIcon" />
        </header>
        {error && (
          <div className="error">
            <span>{error}</span>
            <button onClick={() => setError("")}>
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
              onReview={() => setPage("review")}
              onAsk={() => setAssistant(true)}
            />
          )}
          {page === "review" && (
            <ReviewPage
              rows={filtered}
              selected={selected}
              receipt={receipt}
              loading={loading}
              scope={scope}
              setScope={setScope}
              query={query}
              setQuery={setQuery}
              onChoose={choose}
              onClose={() => {
                setSelected(null);
                setReceipt(null);
              }}
              note={note}
              setNote={setNote}
              onDecide={decide}
              busy={busy}
            />
          )}
          {page === "ledger" && (
            <LedgerPage
              rows={filtered.filter((r) => r.state === "admitted")}
              selected={selected}
              receipt={receipt}
              onChoose={choose}
            />
          )}
          {page === "activity" && <ActivityPage rows={activity} />}
          {page === "admin" && (
            <AdminPage
              credentials={credentials}
              secret={credentialSecret}
              busy={busy}
              onAction={credentialAction}
              onDismissSecret={() => setCredentialSecret("")}
            />
          )}
        </section>
      </main>
      <Dialog.Root open={assistant} onOpenChange={setAssistant}>
        <Dialog.Portal>
          <Dialog.Overlay className="dialogOverlay" />
          <Dialog.Content className="assistant">
            <div className="assistantHead">
              <div>
                <Dialog.Title>Ask Proofpress</Dialog.Title>
                <Dialog.Description>
                  Answers from the current workspace. Advisory only.
                </Dialog.Description>
              </div>
              <Dialog.Close className="iconButton" aria-label="Close assistant">
                <PanelRightClose />
              </Dialog.Close>
            </div>
            <div className="messages">
              {messages.length === 0 ? (
                <div className="assistantEmpty">
                  <Bot />
                  <h3>Ask about governed state</h3>
                  <p>
                    Find what needs review, why a conclusion is supported, or
                    what successor agents may rely on.
                  </p>
                </div>
              ) : (
                messages.map((m, i) => (
                  <div key={i} className={`message ${m.role}`}>
                    {m.role === "assistant" ? (
                      <ReactMarkdown>{m.text}</ReactMarkdown>
                    ) : (
                      m.text
                    )}
                  </div>
                ))
              )}
            </div>
            <div className="composer">
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    ask();
                  }
                }}
                placeholder="Ask about this workspace…"
              />
              <Button onClick={ask}>Send</Button>
            </div>
          </Dialog.Content>
        </Dialog.Portal>
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
        <span>{eyebrow}</span>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {action}
    </div>
  );
}
function HomePage({ pending, admitted, rows, onReview, onAsk }: any) {
  return (
    <div className="pageBody">
      <PageHead
        eyebrow="OWNER WORKSPACE"
        title="Govern what agents can rely on."
        description="Inspect evidence, make human decisions, and carry only admitted knowledge into the next run."
        action={
          <Button onClick={onAsk}>
            <MessageSquareText />
            Ask Proofpress
          </Button>
        }
      />
      <div className="orientation">
        <button onClick={onReview}>
          <span>Needs your review</span>
          <strong>{pending}</strong>
          <small>Candidate conclusions remain excluded</small>
          <ChevronRight />
        </button>
        <div>
          <span>Current ledger</span>
          <strong>{admitted}</strong>
          <small>Admitted conclusions available to agents</small>
          <BookOpen />
        </div>
      </div>
      <section className="section">
        <div className="sectionTitle">
          <h2>Recent knowledge</h2>
          <span>{rows.length} total conclusions</span>
        </div>
        <div className="simpleList">
          {rows.slice(0, 6).map((r: any) => (
            <div key={r.id}>
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
  scope,
  setScope,
  query,
  setQuery,
  onChoose,
  onClose,
  note,
  setNote,
  onDecide,
  busy,
}: any) {
  return (
    <div className="workspacePage">
      <div className="work">
        <PageHead
          eyebrow="GOVERNANCE INBOX"
          title="Review"
          description="Evidence and recommendations inform the decision. Only your approval admits knowledge."
        />
        <div className="filterbar">
          <label>
            <Search />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Filter candidates…"
            />
          </label>
          <input
            className="scopeInput"
            value={scope}
            onChange={(e) => setScope(e.target.value)}
            placeholder="Scope"
          />
          <span>{rows.length} conclusions</span>
        </div>
        <div className="tableWrap">
          <table>
            <thead>
              <tr>
                <th>Conclusion</th>
                <th>Status</th>
                <th>Scope</th>
                <th>Evidence</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row: any) => (
                <tr
                  key={row.id}
                  className={selected === row.id ? "selected" : ""}
                  onClick={() => onChoose(row.id)}
                >
                  <td>
                    <b>{row.label}</b>
                    <small>{row.id}</small>
                  </td>
                  <td>
                    <Badge state={row.state} />
                  </td>
                  <td>{row.scope || "—"}</td>
                  <td>Bound</td>
                  <td>
                    <ChevronRight />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!loading && rows.length === 0 && (
            <div className="empty">No conclusions match this view.</div>
          )}
        </div>
      </div>
      <Inspector
        receipt={receipt}
        onClose={onClose}
        note={note}
        setNote={setNote}
        onDecide={onDecide}
        busy={busy}
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
}: any) {
  if (!r)
    return (
      <aside className="inspector">
        <div className="empty">
          Select a conclusion to inspect its evidence and review state.
        </div>
      </aside>
    );
  const can = r.state === "needs_review";
  return (
    <aside className="inspector">
      <button className="mobileBack" onClick={onClose}>
        ← Back to review
      </button>
      <div className="inspectorTop">
        <span>CONCLUSION</span>
        <Badge state={r.state} />
        <h2>{r.conclusion.statement}</h2>
        <p>
          Proposed by {r.conclusion.proposer || "agent"} ·{" "}
          <span className="mono">{r.conclusion.id}</span>
        </p>
      </div>
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
              <p>{evidenceText(e)}</p>
              <small>Bound to this conclusion</small>
            </article>
          ))}
          {!(r.evidence || []).length && (
            <div className="empty">No bound evidence on this receipt.</div>
          )}
        </Tabs.Content>
        <Tabs.Content value="checks" className="tabContent">
          <div className="checkList">
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
            <span>POLICY / MODEL RECOMMENDATION</span>
            <b>{r.recommendation?.recommendation || "Not configured"}</b>
            <p>
              {r.recommendation?.rationale ||
                "A recommendation cannot admit this conclusion."}
            </p>
          </div>
        </Tabs.Content>
        <Tabs.Content value="history" className="tabContent">
          {(r.history || []).map((h: any, i: number) => (
            <div className="historyRow" key={i}>
              <span></span>
              <div>
                <b>{h.type}</b>
                <small>{h.created_at}</small>
              </div>
            </div>
          ))}
        </Tabs.Content>
      </Tabs.Root>
      {can ? (
        <div className="decision">
          <div>
            <span>HUMAN DECISION</span>
            <p>
              Approval makes this conclusion available to eligible agents in
              scope.
            </p>
          </div>
          <textarea
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
              disabled={busy}
              onClick={() => onDecide("admit")}
            >
              Approve
            </Button>
          </div>
        </div>
      ) : (
        <div className="recorded">
          <Check />
          <div>
            <b>Decision recorded</b>
            <p>
              {r.state === "admitted"
                ? "Available in governed context when current and in scope."
                : "Retained for audit; excluded from governed context."}
            </p>
          </div>
        </div>
      )}
    </aside>
  );
}
function LedgerPage({ rows, selected, receipt, onChoose }: any) {
  return (
    <div className="workspacePage">
      <div className="work pageBody">
        <PageHead
          eyebrow="GOVERNED CONTEXT"
          title="Ledger"
          description="Only admitted, current conclusions appear here."
        />
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
                  onClick={() => onChoose(r.id)}
                >
                  <td>
                    <b>{r.label}</b>
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
              No admitted conclusions yet. Approved, current knowledge will appear here.
            </div>
          )}
        </div>
      </div>
      <Inspector
        receipt={receipt?.state === "admitted" ? receipt : null}
        note=""
        setNote={() => {}}
        onDecide={() => {}}
        busy={false}
      />
    </div>
  );
}
function ActivityPage({ rows }: any) {
  return (
    <div className="pageBody">
      <PageHead
        eyebrow="APPEND-ONLY RECORD"
        title="Activity"
        description="Proposal and decision history visible from the current ledger projection."
      />
      <div className="timeline">
        {rows.slice(0, 20).map((r: any) => (
          <div key={r.audit_id}>
            <span></span>
            <div>
              <Badge state={r.outcome === "ok" ? "recorded" : "blocked"} />
              <b>{(r.operation || "request").replaceAll(".", " · ")}</b>
              <small>
                {r.principal_id || "Unknown principal"} · {r.occurred_at}
              </small>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
function AdminPage({
  credentials,
  secret,
  busy,
  onAction,
  onDismissSecret,
}: any) {
  const [principal, setPrincipal] = React.useState("");
  const [label, setLabel] = React.useState("");
  return (
    <div className="pageBody">
      <PageHead
        eyebrow="OWNER ONLY"
        title="Admin"
        description="Manage the agents that can propose knowledge and read governed context."
        action={null}
      />
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
            Use one credential per revocable agent or device boundary.
          </small>
        </div>
        <input
          value={principal}
          onChange={(e) => setPrincipal(e.target.value)}
          placeholder="agent:claude-code"
          required
        />
        <input
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          placeholder="Claude Code · company laptop"
          required
        />
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
              onClick={() => navigator.clipboard.writeText(secret)}
            >
              Copy
            </Button>
            <Button variant="ghost" onClick={onDismissSecret}>
              Done
            </Button>
          </div>
        </div>
      )}
      <div className="credentialList">
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
