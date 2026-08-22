export function validateAdapter(adapter) {
  const errors = [];
  if (!adapter || typeof adapter !== "object") errors.push("adapter must be an object");
  if (typeof adapter?.id !== "string" || !adapter.id) errors.push("adapter.id is required");
  if (typeof adapter?.testOnly !== "boolean") errors.push("adapter.testOnly must be boolean");
  if (typeof adapter?.invoke !== "function") errors.push("adapter.invoke(request, context) is required");
  if (typeof adapter?.metadata !== "function") errors.push("adapter.metadata() is required");
  if (errors.length) throw new Error(`Adapter contract violation: ${errors.join("; ")}`);
  return adapter;
}
export function validateAdapterResult(result) {
  if (!result || typeof result !== "object") throw new Error("Adapter result must be an object");
  if (typeof result.raw_output !== "string") throw new Error("Adapter result raw_output is required");
  if (!result.telemetry || typeof result.telemetry !== "object") {
    throw new Error("Adapter result telemetry object is required");
  }
  return result;
}
