import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./ui/card";
import { Table, TableBody, TableRow, TableCell, TableHeader, TableHead } from "./ui/table";
import { Separator } from "./ui/separator";
import React from "react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "./ui/accordion";

export type DecisionAudit = {
  backend: string;
  requested_model: string;
  response_model: string;
  mapping_version: string;
  latency_ms: number;
  declared_relation_type?: string;
  answers: Record<string, {type: string; choice?: string; noul?: number; confidence?: number; probabilities?: Record<string, number>}>;
};

const questionLabels: Record<string, string> = {
  evidence_support: "Evidence support",
  scope_valid: "Scope fit",
  criteria_met: "Review criteria",
};
const choiceLabels: Record<string, string> = {accept: "Supports", reject: "Does not support", escalate: "Needs attention"};

export function TypedJudgeAdvice({audit}: {audit?: DecisionAudit}) {
  if (!audit || audit.backend !== "jev") return null;
  const recommendation = audit.answers.recommendation;
  const relationType = audit.answers.relation_type;
  const selectedRelationType = relationType?.choice;
  const selectedRelationProbability = typeof selectedRelationType === "string"
    ? relationType?.probabilities?.[selectedRelationType] : undefined;
  const relationTypeLabel = (value: string) => value.replaceAll("_", " ");
  return <Accordion type="single" collapsible className="reviewDisclosure jevAdvice">
    <AccordionItem value="typed-advice"><AccordionTrigger>Jev review details · experimental</AccordionTrigger>
      <AccordionContent>
        <Card className="jevReviewCard">
          <CardHeader>
            <CardTitle>Powered by Jev</CardTitle>
            <CardDescription>Experimental estimates do not approve claims. Owner review or a separately enabled owner policy decides admission.</CardDescription>
          </CardHeader>
          <CardContent>
            <Table aria-label="Recommendation distribution">
              <TableHeader><TableRow><TableHead>Recommendation</TableHead><TableHead className="text-right">Probability</TableHead></TableRow></TableHeader>
              <TableBody>{["accept", "reject", "escalate"].map(key => {
                const value = recommendation?.probabilities?.[key];
                return typeof value === "number" ? <TableRow key={key}><TableCell>{choiceLabels[key]}</TableCell><TableCell className="text-right tabular-nums">{(value * 100).toFixed(1)}%</TableCell></TableRow> : null;
              })}</TableBody>
            </Table>
            {typeof recommendation?.confidence === "number" && <div className="jevConfidence"><span>Distribution confidence</span><strong>{recommendation.confidence.toFixed(3)}</strong></div>}
            <p className="jevExplanation">Confidence describes the distribution; it is not verified accuracy.</p>
            <Separator className="my-5" />
            <Table aria-label="Evidence assessment">
              <TableHeader><TableRow><TableHead>Evidence assessment</TableHead><TableHead className="text-right">Probability of yes</TableHead></TableRow></TableHeader>
              <TableBody>{Object.entries(questionLabels).map(([key, label]) => typeof audit.answers[key]?.noul === "number" ?
                <TableRow key={key}><TableCell>{label}</TableCell><TableCell className="text-right tabular-nums">{(audit.answers[key].noul! * 100).toFixed(1)}%</TableCell></TableRow> : null)}</TableBody>
            </Table>
            {typeof audit.declared_relation_type === "string" && typeof selectedRelationType === "string" && <>
              <Separator className="my-5" />
              <Table aria-label="Citation relation classification">
                <TableHeader><TableRow><TableHead>Relation classification</TableHead><TableHead>Recorded value</TableHead><TableHead className="text-right">Probability</TableHead></TableRow></TableHeader>
                <TableBody>
                  <TableRow><TableCell>Declared by proposal</TableCell><TableCell>{relationTypeLabel(audit.declared_relation_type)}</TableCell><TableCell className="text-right">—</TableCell></TableRow>
                  <TableRow><TableCell>Jev primary relation</TableCell><TableCell>{relationTypeLabel(selectedRelationType)}</TableCell><TableCell className="text-right tabular-nums">{typeof selectedRelationProbability === "number" ? `${(selectedRelationProbability * 100).toFixed(1)}%` : "—"}</TableCell></TableRow>
                </TableBody>
              </Table>
              <p className="jevExplanation">This is bounded citation advice. A human still decides whether to reject or re-propose a relation.</p>
            </>}
            <small className="jevMetadata">{audit.response_model} · {audit.latency_ms} ms · {audit.mapping_version}. Summary generated from these answers.</small>
          </CardContent>
        </Card>
      </AccordionContent>
    </AccordionItem>
  </Accordion>;
}
