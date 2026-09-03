import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const assets = fileURLToPath(
  new URL("../../../src/proofpress/hosted/static/assets/", import.meta.url),
);

for (const name of readdirSync(assets)) {
  if (!name.endsWith(".js") && !name.endsWith(".css")) continue;
  const path = `${assets}/${name}`;
  const source = readFileSync(path, "utf8");
  writeFileSync(path, source.replace(/[ \t]+$/gm, ""));
}
