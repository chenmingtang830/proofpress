export function paretoFrontier(points, { qualityKey, resourceKey }) {
  validatePoints(points, qualityKey, resourceKey);
  return points.filter((candidate) => !points.some((other) => (
    other.id !== candidate.id
    && other[qualityKey] >= candidate[qualityKey]
    && other[resourceKey] <= candidate[resourceKey]
    && (
      other[qualityKey] > candidate[qualityKey]
      || other[resourceKey] < candidate[resourceKey]
    )
  ))).sort((a, b) => (
    a[resourceKey] - b[resourceKey]
    || b[qualityKey] - a[qualityKey]
    || a.id.localeCompare(b.id)
  ));
}

export function pairedDelta(raw, proofpress, { qualityKey, resourceKeys }) {
  validatePoints([raw, proofpress], qualityKey, resourceKeys[0]);
  for (const key of resourceKeys) validateFinite(raw, key), validateFinite(proofpress, key);
  return {
    quality: proofpress[qualityKey] - raw[qualityKey],
    resources: Object.fromEntries(resourceKeys.map((key) => [key, proofpress[key] - raw[key]])),
  };
}

function validatePoints(points, qualityKey, resourceKey) {
  if (!Array.isArray(points) || points.length === 0) throw new Error("points must be a non-empty array");
  const ids = new Set();
  for (const point of points) {
    if (typeof point?.id !== "string" || !point.id) throw new Error("each point requires an id");
    if (ids.has(point.id)) throw new Error(`duplicate point id: ${point.id}`);
    ids.add(point.id);
    validateFinite(point, qualityKey);
    validateFinite(point, resourceKey);
  }
}

function validateFinite(point, key) {
  if (!Number.isFinite(point?.[key])) throw new Error(`${point?.id ?? "point"}.${key} must be finite`);
}

