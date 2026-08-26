import assert from "node:assert/strict";
import test from "node:test";

import { pairedDelta, paretoFrontier } from "../analysis/pareto.mjs";

test("pareto frontier removes strictly dominated configurations", () => {
  const points = [
    { id: "raw", quality: 0.50, cost: 10 },
    { id: "proofpress", quality: 0.60, cost: 10 },
    { id: "frontier-expensive", quality: 0.75, cost: 20 },
    { id: "dominated", quality: 0.55, cost: 15 },
  ];
  assert.deepEqual(
    paretoFrontier(points, { qualityKey: "quality", resourceKey: "cost" }).map(({ id }) => id),
    ["proofpress", "frontier-expensive"],
  );
});

test("paired delta keeps quality and each resource axis separate", () => {
  assert.deepEqual(pairedDelta(
    { id: "raw", quality: 0.5, cost: 10, tokens: 100 },
    { id: "proofpress", quality: 0.6, cost: 12, tokens: 90 },
    { qualityKey: "quality", resourceKeys: ["cost", "tokens"] },
  ), {
    quality: 0.09999999999999998,
    resources: { cost: 2, tokens: -10 },
  });
});

test("pareto frontier rejects missing telemetry instead of treating it as zero", () => {
  assert.throws(
    () => paretoFrontier([{ id: "incomplete", quality: 0.5, cost: null }], { qualityKey: "quality", resourceKey: "cost" }),
    /must be finite/,
  );
});

