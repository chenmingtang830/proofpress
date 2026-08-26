export function assertResponseEligible(result, {
  label,
  outputCap,
  requestedModel,
  requestedProvider,
}) {
  const telemetry = result?.telemetry ?? {};
  if (telemetry.invocation_error) throw new Error(`${label}: provider invocation failed`);
  if (["length", "content_filter", "error"].includes(telemetry.finish_reason))
    throw new Error(`${label}: provider reported truncated output (${telemetry.finish_reason})`);
  if (Number.isFinite(outputCap) && Number.isFinite(telemetry.output_tokens)
    && telemetry.output_tokens >= outputCap)
    throw new Error(`${label}: output token cap hit (${telemetry.output_tokens}/${outputCap})`);
  if (requestedModel && telemetry.model_reported && telemetry.model_reported !== requestedModel)
    throw new Error(`${label}: model identity mismatch (${requestedModel} requested; ${telemetry.model_reported} reported)`);
  if (requestedProvider && telemetry.serving_provider_reported
    && telemetry.serving_provider_reported !== requestedProvider)
    throw new Error(`${label}: provider identity mismatch (${requestedProvider} requested; ${telemetry.serving_provider_reported} reported)`);
  return result;
}
