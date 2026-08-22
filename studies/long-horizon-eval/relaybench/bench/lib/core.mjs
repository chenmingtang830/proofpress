import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

export const PROJECT_ROOT = path.resolve(import.meta.dirname, "..", "..");

export function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

export async function sha256File(filePath) {
  return sha256(await fs.readFile(filePath));
}

export function canonicalJson(value) {
  return JSON.stringify(sortValue(value));
}

export function sortValue(value) {
  if (Array.isArray(value)) return value.map(sortValue);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value).sort().map((key) => [key, sortValue(value[key])]),
    );
  }
  return value;
}

export async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

export async function writeJson(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, { flag: "wx" });
}

export async function recursiveInventory(root) {
  const output = [];
  async function visit(directory, relative = "") {
    const entries = await fs.readdir(directory, { withFileTypes: true });
    entries.sort((a, b) => a.name.localeCompare(b.name));
    for (const entry of entries) {
      const rel = relative ? `${relative}/${entry.name}` : entry.name;
      const absolute = path.join(directory, entry.name);
      if (entry.isSymbolicLink()) {
        output.push({ path: rel, type: "symlink" });
      } else if (entry.isDirectory()) {
        output.push({ path: rel, type: "directory" });
        await visit(absolute, rel);
      } else if (entry.isFile()) {
        const stat = await fs.stat(absolute);
        output.push({ path: rel, type: "file", bytes: stat.size, sha256: await sha256File(absolute) });
      } else {
        output.push({ path: rel, type: "other" });
      }
    }
  }
  await visit(root);
  return output;
}

export function prohibitedInventoryEntries(inventory, prohibitedNames) {
  const prohibited = new Set(prohibitedNames.map((value) => value.toLowerCase()));
  return inventory.filter((entry) =>
    entry.path.split("/").some((segment) => prohibited.has(segment.toLowerCase())),
  );
}

export function parseStageOutput(raw, expectedStageId) {
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return { valid: false, output: null, reason: "malformed_stage_output_json" };
  }
  const keys = Object.keys(parsed).sort();
  if (keys.join(",") !== "stage_id,test_only,work_product") {
    return { valid: false, output: null, reason: "unexpected_stage_output_shape" };
  }
  if (parsed.stage_id !== expectedStageId || parsed.test_only !== true) {
    return { valid: false, output: null, reason: "stage_output_identity_mismatch" };
  }
  const work = parsed.work_product;
  if (!work || typeof work !== "object" || typeof work.operative_version !== "string" || !work.issues || typeof work.issues !== "object") {
    return { valid: false, output: null, reason: "invalid_stage_work_product" };
  }
  return { valid: true, output: parsed, reason: null };
}
