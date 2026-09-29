# Hosted workspace ownership

For this self-hosted slice, one customer organization maps to one workspace.
`workspace_id` is the ownership key. Authentication resolves it from the
credential or Owner session; an operation body, topic, actor string, URL, or
header cannot select a different workspace. `execute_as()` revalidates the
credential, principal, workspace, role, and current permissions before using
the supplied server-side context.

The SQLite event store and idempotency transaction are scoped to workspace
and principal. Kernel payloads remain unchanged: a content-derived claim or
evidence ID may occur in two workspaces, and projection input must come from
the selected store. OAuth codes and tokens inherit ownership from credentials;
execution attempts inherit it from their parent execution. Database backup is
a deployment operation; `export_bundle()` is a workspace export.

Legacy file and environment policy, OpenRouter key, Owner assistant, and
workspace label belong only to the deployment's designated default workspace.
A control plane with exactly one existing workspace binds it automatically;
bootstrap binds the initial workspace. If a database already contains multiple
workspaces at startup, an operator must supply `legacy_default_workspace_id`
to `HostedControlPlane` or legacy defaults remain disabled. A missing policy
for any other workspace fails closed for governed operations. Its Owner may
save an explicit first policy from a safe, disabled version-zero seed; no
policy or provider key is copied from another workspace.

Execution completion validates attempt, workspace, and principal together.
Execution and Judge recovery process one workspace at a time; startup may
iterate the registered workspaces as a deployment operation. Shared hosting,
customer provisioning, memberships, and new role hierarchy remain disabled.
The two-workspace test fixture proves isolation in a shared SQLite database
without changing production bootstrap behavior. No ownership schema or
historical event migration is required for this slice.
