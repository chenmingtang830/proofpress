#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const args = parseArgs(process.argv.slice(2));
if (!args.file || !args.output) {
  process.stderr.write("Usage: node scripts/bench-generate-proofpress-claims.mjs --file <anchored.md> --output <claims.json>\n");
  process.exit(2);
}

const source = await fs.readFile(path.resolve(args.file), "utf8");
const marker = /^\[\/\/\]: # \(ob:([a-f0-9]{8})\)\s*$/gm;
const matches = [...source.matchAll(marker)];
if (!matches.length) throw new Error(`No Proofpress block anchors found: ${args.file}`);
const claims = matches.map((match, index) => {
  const start = match.index + match[0].length;
  const end = matches[index + 1]?.index ?? source.search(/^\[\/\/\]: # \(proofpress:/m);
  const block = source.slice(start, end < 0 ? source.length : end).trim();
  const preview = block
    .replace(/```[\s\S]*$/m, "code or diagram block")
    .replace(/^#+\s*/, "")
    .replace(/^[-*]\s+/, "")
    .replace(/\s+/g, " ")
    .slice(0, 180) || "portable metadata block";
  return {
    block: match[1],
    kind: "added",
    note: `Added for RelayBench H4 Phase Zero freeze review: ${preview}`,
  };
});

const output = path.resolve(args.output);
await fs.mkdir(path.dirname(output), { recursive: true });
await fs.writeFile(output, `${JSON.stringify(claims, null, 2)}\n`, { flag: "w" });
process.stdout.write(`wrote ${claims.length} added-block claims -> ${output}\n`);

function parseArgs(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--file") values.file = argv[++index];
    else if (argv[index] === "--output") values.output = argv[++index];
    else throw new Error(`Unknown argument: ${argv[index]}`);
  }
  return values;
}
