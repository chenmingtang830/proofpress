import fs from "node:fs/promises";

export async function loadEnvFile(file, base = process.env) {
  if (!file) return { ...base };
  const output = { ...base };
  const body = await fs.readFile(file, "utf8");
  for (const line of body.split(/\r?\n/)) {
    const match = line.match(/^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$/);
    if (!match) continue;
    let value = match[2];
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
    output[match[1]] = value;
  }
  return output;
}
