export type AgentClient = "codex" | "claude" | "cursor";

export function skillInstallation(client: AgentClient) {
  const directory = { codex: ".agents", claude: ".claude", cursor: ".cursor" }[client];
  // A separate shell preserves errexit even when callers chain this command
  // with `&&`. All downloads finish before any installed file is replaced.
  return `sh <<'PROOFPRESS_INSTALL'
set -eu
skill_root=${directory}/skills/proofpress-governed-context
skill_source=https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context
mkdir -p "$(dirname "$skill_root")"
skill_stage=$(mktemp -d "$skill_root.download.XXXXXX")
trap 'rm -rf "$skill_stage"' 0
mkdir -p "$skill_stage/assets" "$skill_stage/scripts"
for file in SKILL.md assets/context-policy.yaml assets/judge-criteria.md scripts/initialize_policy.py; do
  curl -fsSL "$skill_source/$file" -o "$skill_stage/$file"
done
mkdir -p "$skill_root/assets" "$skill_root/scripts"
for file in SKILL.md assets/context-policy.yaml assets/judge-criteria.md scripts/initialize_policy.py; do
  mv -f "$skill_stage/$file" "$skill_root/$file"
done
PROOFPRESS_INSTALL`;
}
