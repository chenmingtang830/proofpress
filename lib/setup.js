"use strict";

const fs = require("node:fs");
const path = require("node:path");

const START = "<!-- proofpress:setup:start -->";
const END = "<!-- proofpress:setup:end -->";
const BADGE_ALT = "Proofpress: verifiable revision history";
const BADGE = `[![${BADGE_ALT}](https://img.shields.io/badge/Proofpress-verifiable_revision_history-5FB3C4)](https://github.com/chenmingtang830/proofpress)`;
const AGENTS = new Set(["codex", "claude", "cursor"]);

function usage() {
  return [
    "usage: proofpress setup [options]",
    "",
    "options:",
    "  --agent <codex|claude|cursor|all>  adapter to install (default: auto)",
    "  --badge <markdown-file>            add a visible Proofpress badge",
    "  --skip-git-config                  do not configure ledger ref syncing",
    "  -h, --help                         show this help"
  ].join("\n");
}

function parseArgs(argv) {
  const result = { agents: [], badge: null, skipGitConfig: false, help: false };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") {
      result.help = true;
    } else if (arg === "--skip-git-config") {
      result.skipGitConfig = true;
    } else if (arg === "--agent") {
      const value = argv[++i];
      if (!value) throw new Error("--agent requires a value");
      result.agents.push(value);
    } else if (arg.startsWith("--agent=")) {
      result.agents.push(arg.slice("--agent=".length));
    } else if (arg === "--badge") {
      result.badge = argv[++i];
      if (!result.badge) throw new Error("--badge requires a Markdown file");
    } else if (arg.startsWith("--badge=")) {
      result.badge = arg.slice("--badge=".length);
    } else {
      throw new Error(`unknown option: ${arg}`);
    }
  }
  return result;
}

function detectAgents(cwd) {
  const detected = [];
  if (fs.existsSync(path.join(cwd, ".claude"))) detected.push("claude");
  if (fs.existsSync(path.join(cwd, ".cursor"))) detected.push("cursor");
  if (fs.existsSync(path.join(cwd, "AGENTS.md"))) detected.push("codex");
  return detected.length ? detected : ["codex"];
}

function normalizeAgents(values, cwd) {
  const expanded = values.length ? values : detectAgents(cwd);
  const normalized = new Set();
  for (const value of expanded) {
    if (value === "all") {
      for (const agent of AGENTS) normalized.add(agent);
    } else if (AGENTS.has(value)) {
      normalized.add(value);
    } else {
      throw new Error(`unsupported agent "${value}"`);
    }
  }
  return [...normalized];
}

function stripCarrierTransport(text) {
  return text
    .split(/\r?\n/)
    .filter((line) => !/^\s*\[\/\/\]: # \((?:ob|proofpress:meta|proofpress:capsule):/.test(line))
    .join("\n")
    .replace(/^<!-- Append to AGENTS\.md.*?-->\s*/s, "")
    .trim();
}

function npmCommands(text) {
  return text
    .replaceAll("python3 proofpress.py", "npx --no-install proofpress")
    .replace(
      "in a repository containing proofpress.py",
      "in a repository configured for Proofpress"
    );
}

function writeIfChanged(target, content) {
  const prior = fs.existsSync(target) ? fs.readFileSync(target, "utf8") : null;
  if (prior === content) return false;
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, content);
  return true;
}

function installCodex(cwd, packageRoot) {
  const target = path.join(cwd, "AGENTS.md");
  const source = fs.readFileSync(
    path.join(packageRoot, "skills", "codex", "AGENTS-snippet.md"),
    "utf8"
  );
  const block = `${START}\n${npmCommands(stripCarrierTransport(source))}\n${END}`;
  const prior = fs.existsSync(target) ? fs.readFileSync(target, "utf8") : "";
  const pattern = new RegExp(`${START}[\\s\\S]*?${END}`, "m");
  const next = pattern.test(prior)
    ? prior.replace(pattern, block)
    : `${prior.trimEnd()}${prior.trim() ? "\n\n" : ""}${block}\n`;
  const changed = writeIfChanged(target, next);
  console.log(`${changed ? "installed" : "already current"}: Codex contract -> AGENTS.md`);
}

function installSkill(cwd, packageRoot, agent) {
  const sourceDir = path.join(packageRoot, "skills", agent === "claude" ? "claude-code" : "cursor", "proofpress");
  const targetDir = agent === "claude"
    ? path.join(cwd, ".claude", "skills", "proofpress")
    : path.join(cwd, ".agents", "skills", "proofpress");
  const files = fs.readdirSync(sourceDir, { withFileTypes: true });
  let changed = false;
  for (const entry of files) {
    if (entry.isDirectory()) {
      const nestedSource = path.join(sourceDir, entry.name);
      const nestedTarget = path.join(targetDir, entry.name);
      fs.mkdirSync(nestedTarget, { recursive: true });
      for (const nested of fs.readdirSync(nestedSource)) {
        const content = fs.readFileSync(path.join(nestedSource, nested), "utf8");
        changed = writeIfChanged(path.join(nestedTarget, nested), content) || changed;
      }
    } else {
      const content = npmCommands(
        entry.name.endsWith(".md")
          ? stripCarrierTransport(fs.readFileSync(path.join(sourceDir, entry.name), "utf8"))
          : fs.readFileSync(path.join(sourceDir, entry.name), "utf8")
      );
      changed = writeIfChanged(path.join(targetDir, entry.name), `${content.trimEnd()}\n`) || changed;
    }
  }
  console.log(`${changed ? "installed" : "already current"}: ${agent} skill -> ${path.relative(cwd, targetDir)}`);
}

function addBadge(cwd, relativeFile) {
  const target = path.resolve(cwd, relativeFile);
  const relative = path.relative(cwd, target);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error("--badge target must be inside the repository");
  }
  if (!/\.md$/i.test(target)) throw new Error("--badge target must be a Markdown file");
  if (!fs.existsSync(target)) throw new Error(`badge target does not exist: ${relativeFile}`);
  const prior = fs.readFileSync(target, "utf8");
  if (prior.includes(BADGE_ALT)) {
    console.log(`already current: badge -> ${relativeFile}`);
    return;
  }
  const lines = prior.split(/\r?\n/);
  let index = 0;
  while (index < lines.length && /^\s*\[\/\/\]: # \(ob:/.test(lines[index])) index += 1;
  if (index < lines.length && /^#\s+/.test(lines[index])) index += 1;
  lines.splice(index, 0, "", BADGE);
  writeIfChanged(target, lines.join("\n"));
  console.log(`installed: badge -> ${relativeFile}`);
}

function writeManifest(cwd, agents) {
  const target = path.join(cwd, ".proofpress", "manifest.json");
  const manifest = {
    schema: 1,
    runtime: "npm",
    package: "proofpress",
    adapters: agents.sort()
  };
  const changed = writeIfChanged(target, `${JSON.stringify(manifest, null, 2)}\n`);
  console.log(`${changed ? "installed" : "already current"}: .proofpress/manifest.json`);
}

function runSetup(argv, options) {
  const parsed = parseArgs(argv);
  if (parsed.help) {
    console.log(usage());
    return { skipGitConfig: true };
  }
  const agents = normalizeAgents(parsed.agents, options.cwd);
  for (const agent of agents) {
    if (agent === "codex") installCodex(options.cwd, options.packageRoot);
    else installSkill(options.cwd, options.packageRoot, agent);
  }
  writeManifest(options.cwd, agents);
  if (parsed.badge) addBadge(options.cwd, parsed.badge);
  console.log("Proofpress setup complete. Portable history remains opt-in per artifact.");
  return { skipGitConfig: parsed.skipGitConfig };
}

module.exports = { runSetup };
