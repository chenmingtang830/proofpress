import React from "react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "./ui/accordion";

export type DecisionAudit = {
  backend: string;
  requested_model: string;
  response_model: string;
  mapping_version: string;
  latency_ms: number;
  answers: Record<string, {type: string; noul?: number; confidence?: number; probabilities?: Record<string, number>}>;
};

const questionLabels: Record<string, string> = {
  evidence_support: "Evidence supports the assertion",
  scope_valid: "Scope is justified by the evidence",
  criteria_met: "Workspace criteria and revision requirements met",
};

export function TypedJudgeAdvice({audit}: {audit?: DecisionAudit}) {
  if (!audit || audit.backend !== "jev") return null;
  const recommendation = audit.answers.recommendation;
  return <Accordion type="single" collapsible className="reviewDisclosure">
    <AccordionItem value="typed-advice"><AccordionTrigger>Jev structured advice · experimental</AccordionTrigger>
      <AccordionContent>
        <p>These are model estimates, not verified accuracy or permission to reuse. Human Approval remains required.</p>
        <dl className="decisionStack">
          {Object.entries(recommendation?.probabilities || {}).map(([label, value]) =>
            <div key={label}><dt>Probability · {label}</dt><dd>{(value * 100).toFixed(1)}%</dd></div>)}
          {typeof recommendation?.confidence === "number" && <div><dt>Distribution confidence</dt><dd>{recommendation.confidence.toFixed(3)}</dd></div>}
          {Object.entries(questionLabels).map(([key, label]) => typeof audit.answers[key]?.noul === "number" ?
            <div key={key}><dt>{label} · probability of yes</dt><dd>{(audit.answers[key].noul! * 100).toFixed(1)}%</dd></div> : null)}
        </dl>
        <small>{audit.response_model} · {audit.latency_ms} ms · {audit.mapping_version}. The accompanying rationale is a template summary of these answers.</small>
      </AccordionContent>
    </AccordionItem>
  </Accordion>;
}
