#!/usr/bin/env node
import readline from "node:readline";
import { invokeDeterministicStage, testOnlyMetadata } from "../adapters/deterministic-test.mjs";

const lines = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
for await (const line of lines) {
  if (!line.trim()) continue;
  let request;
  try {
    request = JSON.parse(line);
    const result = await invokeDeterministicStage({
      workspace: process.cwd(),
      stageId: request.stage_id,
      verifierEvidence: request.verifier_evidence,
    });
    process.stdout.write(`${JSON.stringify({ request_id: request.request_id, ok: true, result, metadata: testOnlyMetadata() })}\n`);
  } catch (error) {
    process.stdout.write(`${JSON.stringify({ request_id: request?.request_id ?? null, ok: false, error: error.message })}\n`);
  }
}
