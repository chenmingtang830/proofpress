import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { spawnSync } from "node:child_process";
import { describe, it, expect } from "vitest";
import { skillInstallation, type AgentClient } from "./skill-installation";

const files = ["SKILL.md", "assets/context-policy.yaml", "assets/judge-criteria.md", "scripts/initialize_policy.py"];

function fixture() {
  const root = mkdtempSync(join(tmpdir(), "proofpress skill install "));
  const bin = join(root, "bin");
  mkdirSync(bin);
  // Simulate curl truncating its destination before a network/HTTP failure.
  writeFileSync(join(bin, "curl"), `#!/bin/sh
count=0
if [ -f "$DOWNLOAD_COUNT" ]; then count=$(cat "$DOWNLOAD_COUNT"); fi
count=$((count + 1))
printf '%s' "$count" > "$DOWNLOAD_COUNT"
while [ "$#" -gt 0 ]; do
  if [ "$1" = -o ]; then shift; output=$1; else url=$1; fi
  shift
done
printf 'download:%s' "$url" > "$output"
if [ "$count" = "$FAIL_AT" ]; then printf partial > "$output"; exit 22; fi
`, { mode: 0o755 });
  const run = (client: AgentClient, failAt = 0) => spawnSync("sh", ["-c",
    `{\n${skillInstallation(client)}\n} && printf connected > mcp-started`,
  ], { cwd: root, encoding: "utf8", env: { ...process.env, PATH: `${bin}:${process.env.PATH}`, DOWNLOAD_COUNT: join(root, "downloads"), FAIL_AT: String(failAt) } });
  return { root, run, cleanup: () => rmSync(root, { recursive: true, force: true }) };
}

describe("skill installation shell command", () => {
  it.each([["codex", ".agents"], ["claude", ".claude"], ["cursor", ".cursor"]] as const)("installs all files for %s before continuing", (client, directory) => {
    const f = fixture();
    try {
      const target = join(f.root, directory, "skills", "proofpress-governed-context");
      mkdirSync(target, { recursive: true });
      writeFileSync(join(target, "custom.md"), "local customization");
      const result = f.run(client);
      expect(result.status, result.stderr).toBe(0);
      for (const file of files) expect(readFileSync(join(target, file), "utf8")).toContain(`/main/.agents/skills/proofpress-governed-context/${file}`);
      expect(readFileSync(join(target, "custom.md"), "utf8")).toBe("local customization");
      expect(existsSync(join(f.root, "mcp-started"))).toBe(true);
      expect(readdirSync(dirname(target))).toEqual(["proofpress-governed-context"]);
    } finally { f.cleanup(); }
  });

  for (const existing of [false, true]) {
    it.each([1, 2, 3, 4])(`fails closed on download %i with ${existing ? "an existing" : "no existing"} installation`, failAt => {
      const f = fixture();
      try {
        const target = join(f.root, ".agents", "skills", "proofpress-governed-context");
        if (existing) {
          for (const file of files) {
            mkdirSync(dirname(join(target, file)), { recursive: true });
            writeFileSync(join(target, file), `original:${file}`);
          }
        }
        const result = f.run("codex", failAt);
        expect(result.status, result.stderr).toBe(22);
        expect(existsSync(join(f.root, "mcp-started"))).toBe(false);
        if (existing) {
          for (const file of files) expect(readFileSync(join(target, file), "utf8")).toBe(`original:${file}`);
        } else expect(existsSync(target)).toBe(false);
        expect(readdirSync(dirname(target))).toEqual(existing ? ["proofpress-governed-context"] : []);
      } finally { f.cleanup(); }
    });
  }
});
