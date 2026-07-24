#!/usr/bin/env node
"use strict";

const path = require("node:path");
const { runPython } = require("../lib/python");
const { runSetup } = require("../lib/setup");

const packageRoot = path.resolve(__dirname, "..");
const args = process.argv.slice(2);

if (args[0] === "setup") {
  try {
    const result = runSetup(args.slice(1), { packageRoot, cwd: process.cwd() });
    if (!result.skipGitConfig) {
      const status = runPython(["init"], { packageRoot, cwd: process.cwd() });
      if (status !== 0) process.exit(status);
    }
  } catch (error) {
    console.error(`proofpress setup: ${error.message}`);
    process.exit(1);
  }
} else {
  process.exit(runPython(args, { packageRoot, cwd: process.cwd() }));
}
