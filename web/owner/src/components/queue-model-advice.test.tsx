import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { QueueModelAdvice } from "./queue-model-advice";

describe("review queue model advice", () => {
  it.each([
    ["accept", "Suggest approve", "accent-soft"],
    ["escalate", "Suggest escalate", "attention-bg"],
    ["reject", "Suggest reject", "del-bg"],
  ])("labels %s as advice rather than an admission", (recommendation, label, color) => {
    const html = renderToStaticMarkup(<QueueModelAdvice review={{ state: "current", recommendation }} />);
    expect(html).toContain(label);
    expect(html).toContain(color);
    expect(html).not.toContain("Admitted");
  });

  it.each([
    ["stale", "Refresh required"], ["queued", "Queued"], ["running", "Reviewing…"],
    ["failed", "Review failed"], ["interrupted", "Review interrupted"],
    ["skipped", "Review skipped"], ["blocked", "Checks need correction"], ["off", "AI review off"],
    ["completed", "No advice recorded"],
  ])("never presents previous advice as current while %s", (state, label) => {
    const html = renderToStaticMarkup(<QueueModelAdvice review={{ state, recommendation: "accept" }} />);
    expect(html).toContain(label);
    expect(html).not.toContain("Suggest approve");
  });

  it("keeps missing or unrecognized advice neutral", () => {
    for (const review of [undefined, { state: "current", recommendation: "unknown" }]) {
      expect(renderToStaticMarkup(<QueueModelAdvice review={review} />)).toContain("Not run yet");
    }
  });
});
