"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

function pythonCandidates() {
  if (process.env.PROOFPRESS_PYTHON) {
    return [[process.env.PROOFPRESS_PYTHON, []]];
  }
  if (process.platform === "win32") {
    return [["py", ["-3"]], ["python", []]];
  }
  return [["python3", []], ["python", []]];
}

function runPython(args, options) {
  const cli = path.join(options.packageRoot, "proofpress.py");
  if (!fs.existsSync(cli)) {
    console.error(`proofpress: bundled CLI not found: ${cli}`);
    return 1;
  }

  for (const [command, prefix] of pythonCandidates()) {
    const result = spawnSync(command, [...prefix, cli, ...args], {
      cwd: options.cwd,
      stdio: "inherit",
      env: process.env
    });
    if (!result.error) return result.status === null ? 1 : result.status;
    if (result.error.code !== "ENOENT") {
      console.error(`proofpress: could not start ${command}: ${result.error.message}`);
      return 1;
    }
  }

  console.error(
    "proofpress requires Python 3. Install Python 3 or set PROOFPRESS_PYTHON " +
    "to the Python 3 executable."
  );
  return 1;
}

module.exports = { runPython };
