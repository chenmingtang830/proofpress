import fs from "node:fs/promises";
import path from "node:path";

export async function loadRunRecords(directory) {
  const records = [];
  for (const name of (await fs.readdir(directory)).sort()) {
    if (!name.endsWith(".json")) continue;
    const parsed = JSON.parse(await fs.readFile(path.join(directory, name), "utf8"));
    if (parsed.record_type === "h4_calibration_episode") records.push(parsed);
  }
  return records;
}
