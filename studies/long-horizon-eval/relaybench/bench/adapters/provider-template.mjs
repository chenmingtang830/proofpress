import { validateAdapter } from "./adapter-contract.mjs";

export async function createAdapter(frozenConfig) {
  return validateAdapter({
    id: "UNCONFIGURED/provider-template",
    testOnly: false,
    metadata() {
      return {
        provider: frozenConfig.provider,
        route: frozenConfig.route,
        resolved_model: frozenConfig.resolved_model,
        reasoning_effort: frozenConfig.reasoning_effort,
        temperature: frozenConfig.temperature,
        seed: frozenConfig.seed,
        provider_fallback: false,
        cross_provider_retries: false,
      };
    },
    async invoke() {
      throw new Error(
        "Provider template is intentionally unconfigured. Implement one provider call here, return the contract shape, and do not add fallback or cross-provider retries.",
      );
    },
  });
}
