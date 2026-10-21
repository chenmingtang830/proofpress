import { Badge } from "@/components/ui/badge";

export type QueueModelReview = {
  state: string;
  recommendation?: string | null;
  model?: string | null;
};

export function QueueModelAdvice({ review }: { review?: QueueModelReview }) {
  const verdict = review?.recommendation;
  if (review?.state === "current" && verdict && ["accept", "escalate", "reject"].includes(verdict)) {
    const label = { accept: "Suggest approve", escalate: "Suggest escalate", reject: "Suggest reject" }[verdict];
    return <Badge state={verdict}>{label}</Badge>;
  }
  const label = ({
    queued: "Queued", running: "Reviewing…", failed: "Review failed",
    interrupted: "Review interrupted", skipped: "Review skipped",
    blocked: "Checks need correction", stale: "Refresh required", off: "AI review off",
    completed: "No advice recorded",
  } as Record<string, string>)[review?.state || ""] || "Not run yet";
  return <span className="queueModelState">{label}</span>;
}
