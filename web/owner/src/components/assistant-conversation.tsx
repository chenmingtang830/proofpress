import React from "react";
import ReactMarkdown from "react-markdown";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export type AssistantMessage = { role: string; text: string };
export type ConversationProps = {
  messages: AssistantMessage[];
  question: string;
  setQuestion: (value: string) => void;
  onSend: () => void;
  pending: boolean;
};

export function AssistantConversation({ messages, question, setQuestion, onSend, pending }: ConversationProps) {
  const input = React.useRef<HTMLTextAreaElement>(null);
  const end = React.useRef<HTMLDivElement>(null);
  React.useEffect(() => {
    end.current?.scrollIntoView({ block: "nearest" });
  }, [messages.length, pending]);
  return <>
    {messages.length > 0 && <div className="messages" role="log" aria-label="Assistant conversation" aria-live="polite">
      {messages.map((m, i) => <div key={i} className={`message ${m.role}`}>
        <span className="messageAuthor">{m.role === "user" ? "You" : "Proofpress"}</span>
        {m.role === "assistant" ? <ReactMarkdown>{m.text}</ReactMarkdown> : m.text}
      </div>)}
      {pending && <p role="status">Reading workspace context…</p>}
      <div ref={end} />
    </div>}
    {messages.length === 0 && <div className="suggestedQuestions" aria-label="Suggested questions">
      {["What needs my review?", "Which conclusions are admitted?", "Explain the approval boundary."].map(q =>
        <Button key={q} variant="outline" onClick={() => { setQuestion(q); input.current?.focus(); }}>{q}</Button>
      )}
    </div>}
    <form className="chatComposer" onSubmit={e => { e.preventDefault(); onSend(); }}>
      <Textarea ref={input} aria-label="Ask Proofpress" value={question}
        onChange={e => setQuestion(e.target.value)} placeholder="Ask about this workspace…"
        onKeyDown={e => {
          if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
            e.preventDefault(); onSend();
          }
        }} />
      <div className="composerActions">
        <span>Advisory only. You decide what becomes trusted.</span>
        <Button type="submit" disabled={pending || !question.trim()}>{pending ? "Thinking…" : "Send"}</Button>
      </div>
    </form>
  </>;
}
