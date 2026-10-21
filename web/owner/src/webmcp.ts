import { flushSync } from "react-dom";
import { claimDisplayTitle } from "./components/claim-display";
import { parseCaptureDraft } from "./components/capture-rules";

// Same-origin tools share the visible workflow; privileged mutations remain in human forms.
export function createOwnerTools({api, csrfRef, selectionRequest, setSelected, setNote, setReceipt, setPage, setFullReview, setReloadVersion, setAdminSection, navigate, openReview}: any) {
    const toolText = (value: unknown): {content: {type: string; text: string}[]; isError?: boolean} => ({
      content: [{ type: "text", text: JSON.stringify(value, null, 2) }],
    });
    const tools = [
      {
        name: "get_workspace_summary",
        description: "Summarize the signed-in workspace, review queue, and current governed context without changing state.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: {} },
        execute: async () => {
          const paths = ["/owner/api/graph", "/owner/api/context", "/owner/api/summary"];
          const results = await Promise.allSettled(paths.map(path => api(path)));
          const [graph, context, summary] = results.map(result => result.status === "fulfilled" ? result.value : null);
          const unavailable = results.flatMap((result, index) => result.status === "rejected" ? [{
            section: ["graph", "context", "review"][index], code: result.reason?.code || "request_failed",
            message: result.reason?.message || "Unavailable",
          }] : []);
          const claims = graph ? (graph.nodes || []).filter((node: any) => node.type === "claim") : null;
          return toolText({
            partial: unavailable.length > 0,
            unavailable,
            review: summary,
            current_governed_context_count: context ? (context.governed_context || []).length : null,
            staged_draft_candidate_count: context ? (context.staged_context || []).length : null,
            claim_states: claims ? claims.reduce((counts: Record<string, number>, row: any) => { counts[row.state] = (counts[row.state] || 0) + 1; return counts; }, {}) : null,
            needs_reassessment_count: claims ? claims.filter((row: any) => row.state === "dependency_invalidated").length : null,
            authority: "Agents may inspect and prepare work. Agent approval is never available.",
          });
        },
      },
      {
        name: "get_workspace_identity",
        description: "Read the signed-in workspace identity, role and configuration status without CSRF tokens or credentials.",
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        inputSchema: { type: "object", properties: {}, additionalProperties: false },
        execute: async () => {
          const {workspace_id, workspace, principal, role, review_policy_configured, capabilities} = await api("/owner/api/session");
          return toolText({workspace_id, workspace, principal, role, review_policy_configured, capabilities});
        },
      },
      {
        name: "get_workspace_dashboard",
        description: "Read the same bounded workspace dashboard shown on Home, including open work and usage summaries.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: {}, additionalProperties: false },
        execute: async () => toolText(await api("/owner/api/dashboard")),
      },
      {
        name: "list_runs",
        description: "List recorded agent runs, optionally filtered by status. This does not run or schedule an agent.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: { status: { type: "string" }, limit: { type: "integer", minimum: 1, maximum: 100 } } },
        execute: async ({status = "", limit = 50}: any) => toolText(await api(`/owner/api/runs?status=${encodeURIComponent(status)}&limit=${encodeURIComponent(String(limit))}`)),
      },
      {
        name: "get_run",
        description: "Read one recorded agent run and its attached evidence and findings. Does not change run state.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: {run_id: {type: "string"}}, required: ["run_id"] },
        execute: async ({run_id}: any) => toolText(await api(`/owner/api/runs/${encodeURIComponent(run_id)}`)),
      },
      {
        name: "get_technical_logs",
        description: "Read bounded, server-redacted technical operation metadata. Does not return raw private traces or credentials.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: { limit: { type: "integer", minimum: 1, maximum: 100 } } },
        execute: async ({limit = 50}: any) => toolText(await api(`/owner/api/technical-logs?limit=${encodeURIComponent(String(limit))}`)),
      },
      {
        name: "get_executions",
        description: "Read recorded tool execution receipts shown in Activity. Does not execute operations.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: { limit: { type: "integer", minimum: 1, maximum: 100 } } },
        execute: async ({limit = 50}: any) => toolText(await api(`/owner/api/executions?limit=${encodeURIComponent(String(limit))}`)),
      },
      {
        name: "get_claim_graph",
        description: "Read the bounded evidence, claim, lifecycle, and relation graph for the owner workspace. This does not change state.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: { scope: { type: "string" } } },
        execute: async ({ scope = "" }: any) =>
          toolText(await api(`/owner/api/graph?scope=${encodeURIComponent(scope)}`)),
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
          "Retrieve approved claims and a separate staged_context list. Staged candidates are for clearly marked drafts only, never approved reliance. Does not approve claims.",
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
            withdrawal: r.withdrawal,
            dependency_impact: r.dependency_impact,
            dependent_impact: r.dependent_impact,
            dependencies: r.dependencies,
            relations: r.relations,
            relation_advice: r.relation_advice,
            history: r.history,
          });
        },
      },
      {
        name: "open_claim_lifecycle",
        description: "Open an owner-only withdrawal or dependency-reassessment surface for one claim. Navigation does not record a decision.",
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        inputSchema: {
          type: "object",
          properties: {
            claim_id: { type: "string" },
            action: { type: "string", enum: ["withdraw", "reassess"] },
          },
          required: ["claim_id", "action"],
        },
        execute: async ({ claim_id, action }: any) => {
          const request = ++selectionRequest.current;
          const result = await api(`/owner/api/claims/${encodeURIComponent(claim_id)}`);
          if (request !== selectionRequest.current) throw new Error("The selected claim changed before the lifecycle surface opened");
          const actionAllowed = action === "reassess"
            ? result.state === "dependency_invalidated"
            : ["admitted", "dependency_invalidated"].includes(result.state);
          if (!actionAllowed) throw new Error(`${action} is not available for a claim in state ${result.state}`);
          setNote("");
          setSelected(claim_id);
          setReceipt(result);
          setPage(action === "reassess" ? "review" : "ledger");
          setFullReview(action === "reassess");
          return toolText({
            opened: true,
            action,
            claim_id,
            state: result.state,
            decision_recorded: false,
            requires_human_owner: true,
            url: `${location.origin}/${action === "reassess" ? "review" : "ledger"}?claim_id=${encodeURIComponent(claim_id)}${action === "reassess" ? "&view=full" : ""}`,
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
          setReloadVersion((version: number) => version + 1);
          return toolText({ claim_id, evaluation: result.evaluation, human_approval_recorded: false, next: result.review_policy?.require_judge ? "Model advice is required by policy. Admission still requires an owner decision or a separately enabled Owner policy." : "Open the review surface or check whether the Owner policy is configured to admit qualifying new claims." });
        },
      },
      {
        name: "open_review",
        description: "Open a claim in the owner review surface. Navigation does not make a decision.",
        annotations: { readOnlyHint: true, untrustedContentHint: false },
        inputSchema: { type: "object", properties: { claim_id: { type: "string" }, full: { type: "boolean" } }, required: ["claim_id"] },
        execute: async ({ claim_id, full = true }: any) => {
          if (typeof claim_id !== "string" || !claim_id.trim() || typeof full !== "boolean") throw new Error("Provide a claim ID and a boolean full-view setting.");
          const receipt = await openReview(claim_id, full);
          if (receipt?.claim?.id !== claim_id) throw new Error("The requested claim receipt did not open.");
          return toolText({ opened: true, receipt_claim_id: receipt.claim.id, decision_recorded: false, url: `${location.origin}/review?claim_id=${encodeURIComponent(claim_id)}${full ? "&view=full" : ""}` });
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
            next: "Use the connected agent MCP or CLI to submit supporting evidence and a revision proposal; only an owner decision or explicitly enabled owner policy can approve it.",
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
        name: "get_capture_policy",
        description: "Read versioned knowledge capture guidance and its limits. Guidance does not grant admission authority.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type: "object", properties: {}, additionalProperties: false },
        execute: async () => toolText(await api("/owner/api/capture-policy")),
      },
      {
        name: "prepare_capture_policy_change",
        description: "Load knowledge capture rules into Admin for human review. Never saves policy, submits findings, or schedules research.",
        annotations: { readOnlyHint: false, untrustedContentHint: true },
        inputSchema: {
          type: "object", additionalProperties: false,
          properties: {
            purpose: { type: "string", minLength: 1, maxLength: 1000 },
            capture: { type: "array", minItems: 1, maxItems: 30, items: { type: "string", minLength: 1, maxLength: 500 } },
            exclude: { type: "array", maxItems: 30, items: { type: "string", minLength: 1, maxLength: 500 } },
          },
          required: ["purpose", "capture", "exclude"],
        },
        execute: async (settings: any) => {
          const draft = parseCaptureDraft(JSON.stringify(settings));
          sessionStorage.setItem("proofpress:capture-policy-draft", JSON.stringify(draft));
          window.dispatchEvent(new Event("proofpress:capture-policy-draft"));
          setAdminSection("rules");
          navigate("admin", "?section=rules");
          return toolText({prepared: true, activated: false, requires_human_owner: true,
            next: "Review every capture rule in Admin, then select Save capture rules.",
            url: `${location.origin}/admin?section=rules`});
        },
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
        name: "get_policy_history",
        description: "Read saved capture-rule or review-criteria versions with author and timestamp. Read-only, scoped to the signed-in workspace; no provider secrets or historical executable configuration are returned. Does not restore, save or approve anything.",
        annotations: { readOnlyHint: true, untrustedContentHint: true },
        inputSchema: { type:"object", properties:{kind:{type:"string",enum:["capture","criteria"]},limit:{type:"integer",minimum:1,maximum:50},before_version:{type:"integer",minimum:1}}, required:["kind"], additionalProperties:false },
        execute: async ({kind,limit=10,before_version}:any)=>{
          if (!["capture","criteria"].includes(kind) || !Number.isInteger(limit) || limit < 1 || limit > 50 || (before_version !== undefined && (!Number.isInteger(before_version) || before_version < 1))) throw new Error("Use a valid policy kind, limit and version cursor.");
          const endpoint = kind === "capture" ? "/owner/api/capture-policy/history" : "/owner/api/review-criteria/history";
          return toolText(await api(`${endpoint}?limit=${limit}${before_version === undefined ? "" : `&before_version=${before_version}`}`));
        },
      },
      {
        name: "prepare_review_criteria",
        description: "Stage review criteria in Admin without changing AI, credentials, processing consent or approval settings. A human Owner must save; this tool never saves or authorizes.",
        annotations: { readOnlyHint: false, untrustedContentHint: false },
        inputSchema: { type: "object", properties: { criteria: { type: "string", maxLength: 8000 } }, required: ["criteria"], additionalProperties: false },
        execute: async ({ criteria }: any) => {
          if (typeof criteria !== "string" || criteria.length > 8000) throw new Error("Provide review criteria of at most 8,000 characters.");
          sessionStorage.setItem("proofpress:review-policy-draft", JSON.stringify({ criteria }));
          setAdminSection("models");
          navigate("admin", "?section=models");
          window.dispatchEvent(new Event("proofpress:review-criteria-draft"));
          return toolText({ prepared:true, activated:false, requires_human_owner:true,
            next:"Review the criteria in Admin and select Save review criteria. AI settings remain separate.",
            url:`${location.origin}/admin?section=models` });
        },
      },
      {
        name: "prepare_review_policy_change",
        description:
          "Prepare a review-policy change in Admin for the human owner to inspect and activate. This never saves or authorizes the change.",
        annotations: { readOnlyHint: false, untrustedContentHint: false },
        inputSchema: {
          type: "object", additionalProperties: false,
          properties: {
            provider: { type: "string", description: "Use a provider ID from get_review_policy().providers, including hosted providers when available." },
            endpoint: { type: "string" },
            model: { type: "string" },
            criteria: { type: "string", maxLength: 8000 },
            rubric: { type: "string", description: "Optional current rubric version from get_review_policy(); cannot change the review contract." },
            zdr: { type: "boolean" },
            mode: { type: "string", enum: ["off", "manual", "automatic"] },
            require_judge: { type: "boolean" },
            external_consent: { type: "boolean" },
            auto_admit_new_claims: { type: "boolean", description: "Propose whether a saved Owner policy should automatically approve qualifying new claims workspace-wide. Off by default; the owner must review and save this setting." },
          },
          required: ["provider", "endpoint", "model", "criteria", "zdr", "mode", "require_judge", "external_consent"],
        },
        execute: async (settings: any) => {
          const fields = ["provider", "endpoint", "model", "criteria", "rubric", "zdr", "mode", "require_judge", "external_consent", "auto_admit_new_claims"];
          if (!settings || Object.keys(settings).some(key => !fields.includes(key))) throw new Error("Only review-policy fields are allowed; never supply credentials.");
          for (const key of ["provider", "endpoint", "model", "criteria"]) {
            if (typeof settings[key] !== "string") throw new Error(`${key} must be a string.`);
          }
          if (settings.criteria.length > 8000 || settings.model.length > 160) throw new Error("Review criteria or model exceeds its supported length.");
          for (const key of ["zdr", "require_judge", "external_consent"]) {
            if (typeof settings[key] !== "boolean") throw new Error(`${key} must be boolean.`);
          }
          if (settings.auto_admit_new_claims !== undefined && typeof settings.auto_admit_new_claims !== "boolean") throw new Error("auto_admit_new_claims must be boolean.");
          if (!["off", "manual", "automatic"].includes(settings.mode)) throw new Error("Choose off, manual or automatic mode.");
          const policy = await api("/owner/api/review-policy");
          if (settings.rubric !== undefined && settings.rubric !== policy.settings?.rubric) throw new Error("Keep the current review rubric version.");
          if (!Object.hasOwn(policy.providers || {}, settings.provider)) throw new Error("Choose a provider from get_review_policy().providers.");
          sessionStorage.setItem("proofpress:review-policy-draft", JSON.stringify(settings));
          window.dispatchEvent(new Event("proofpress:review-policy-draft"));
          setAdminSection("models");
          navigate("admin", "?section=models");
          return toolText({
            prepared: true,
            activated: false,
            requires_human_owner: true,
            next: settings.mode === "off"
              ? "Review the prepared manual-review settings and criteria in Admin, then choose Use manual review or Save changes. No provider key or external processing consent is needed while AI is off."
              : "Review the provider, criteria and processing disclosure in Admin, then choose Enable AI checks or Save changes yourself. Hosted verification must be available; enter a key privately only if you choose your own provider.",
            url: `${location.origin}/admin?section=models`,
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
        inputSchema: { type: "object", additionalProperties: false, properties: { principal_id: { type: "string", minLength: 1 }, label: { type: "string", minLength: 1 } }, required: ["principal_id", "label"] },
        execute: async (settings: any) => {
          if (!settings || Object.keys(settings).some(key => !["principal_id", "label"].includes(key)) ||
              typeof settings.principal_id !== "string" || !settings.principal_id.trim() ||
              typeof settings.label !== "string" || !settings.label.trim()) throw new Error("Provide only a non-empty agent identity and key label; never provide credentials.");
          const draft = {principal_id: settings.principal_id.trim(), label: settings.label.trim()};
          sessionStorage.setItem("proofpress:agent-credential-draft", JSON.stringify(draft));
          // Complete this external browser-tool call after mounted form state is
          // committed, including a recipient switch from Reviewer back to Agent.
          flushSync(() => {
            window.dispatchEvent(new Event("proofpress:agent-credential-draft"));
            setAdminSection("access");
            navigate("admin", "?section=access");
          });
          return toolText({ prepared: true, ...draft, issued: false, requires_human_owner: true, secret_exposed_to_agent: false, url: `${location.origin}/admin?section=access` });
        },
      },
    ];

    return tools.map(tool => ({...tool, execute: async (input: any = {}) => {
      try { return await tool.execute(input); }
      catch (error: any) { return {...toolText({error: {code: error.code || "tool_failed", message: error.message || "Tool failed"}}), isError: true}; }
    }}));
}
