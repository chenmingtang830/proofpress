import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { AssistantConversation } from "./components/assistant-conversation";

const base = { messages: [], question: "", setQuestion: () => {}, onSend: () => {}, pending: false };
describe("shared assistant entry", () => {
  it("renders a directly accessible composer and bounded suggestions", () => {
    const html = renderToStaticMarkup(<AssistantConversation {...base} />);
    expect(html).toContain('aria-label="Ask Proofpress"');
    expect(html).toContain("What needs my review?");
    expect(html).toContain("Advisory only.");
    expect(html).toContain('disabled=""');
  });
  it("renders the supplied conversation and pending state", () => {
    const html = renderToStaticMarkup(<AssistantConversation {...base} pending messages={[
      { role: "user", text: "Review my context" },
      { role: "assistant", text: "**Human review** is required." },
    ]} />);
    expect(html).toContain('role="log"');
    expect(html).toContain("<strong>Human review</strong>");
    expect(html).toContain("Thinking…");
    expect(html).not.toContain("Suggested questions");
  });
});
