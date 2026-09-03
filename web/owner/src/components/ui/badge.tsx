import { cn } from "@/lib/utils";
export function Badge({
  state,
  className,
}: {
  state: string;
  className?: string;
}) {
  const value = ({accept: "Evidence supported", reject: "Evidence not supported", escalate: "Needs attention", unresolved: "Needs revalidation"} as Record<string,string>)[state] || state.replaceAll("_", " ");
  return (
    <span
      className={cn(
        "inline-flex h-6 shrink-0 items-center justify-center whitespace-nowrap rounded-full border px-2.5 text-[11px] leading-none font-medium capitalize",
        state === "admitted" || state === "active"
          ? "border-[var(--line)] bg-[var(--add-bg)] text-[var(--add)]"
          : state === "needs_revision"
            ? "border-[var(--line)] bg-[var(--revision-bg)] text-[var(--revision)]"
          : ["needs_review", "accept", "escalate", "unresolved", "evidence_supported", "needs_attention", "retrieved"].includes(state)
            ? "border-[var(--line)] bg-[var(--accent-soft)] text-[var(--accent)]"
          : ["rejected", "blocked", "revoked", "reject", "evidence_not_supported"].includes(state)
            ? "border-[var(--line)] bg-[var(--del-bg)] text-[var(--del)]"
            : "border-[var(--line)] bg-[var(--wash)] text-[var(--ink-2)]",
        className,
      )}
    >
      {value}
    </span>
  );
}
