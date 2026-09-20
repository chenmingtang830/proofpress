import React from "react";
import { Badge } from "./ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { TypedJudgeAdvice, type DecisionAudit } from "./typed-judge-advice";

export type RelationAdvice = {
  relation: {id:string; from:string; to:string; type:string; qualifiers?:Record<string, unknown>};
  state: string;
  recommendation?: {recommendation:string; rationale?:string; decision_audit?:DecisionAudit};
  evaluation?: {checks?:Record<string, boolean>};
};

export function RelationAdvicePanel({items}:{items?:RelationAdvice[]}) {
  if (!items?.length) return null;
  return <section className="relationAdvice" aria-label="Relation model advice">
    {items.map(({relation, state, recommendation}) => <Card key={relation.id}>
      <CardHeader>
        <div className="flex items-center justify-between gap-3">
          <CardTitle>Citation relation advice</CardTitle>
          <Badge state={recommendation?.recommendation || state} />
        </div>
        <CardDescription>
          {relation.type.replaceAll("_", " ")} · <span className="mono">{relation.id}</span>
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {recommendation?.rationale && <p className="text-sm leading-6">{recommendation.rationale}</p>}
        <TypedJudgeAdvice audit={recommendation?.decision_audit} />
      </CardContent>
    </Card>)}
  </section>;
}
