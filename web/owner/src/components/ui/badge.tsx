import { cn } from "@/lib/utils";
import type { ReactNode } from "react";
export function Badge({
  state,
  className,
  children,
}: {
  state: string;
  className?: string;
  children?: ReactNode;
}) {
  const value = ({accept: "Evidence supported", reject: "Evidence not supported", escalate: "Needs attention", unresolved: "Needs revalidation", dependency_invalidated: "Dependency changed", withdrawn: "Withdrawn", retired: "Retired"} as Record<string,string>)[state] || state.replaceAll("_", " ");
  return (
    <span
      data-slot="badge"
      className={cn(
        "inline-flex h-6 shrink-0 items-center justify-center whitespace-nowrap rounded-full border px-2.5 font-['DM_Sans'] text-[11px] leading-none font-medium capitalize",
        state === "admitted" || state === "active"
          ? "border-[var(--line)] bg-[var(--add-bg)] text-[var(--add)]"
          : state === "needs_revision"
            ? "border-[var(--line)] bg-[var(--revision-bg)] text-[var(--revision)]"
          : ["escalate", "needs_attention"].includes(state)
            ? "border-[var(--line)] bg-[var(--attention-bg)] text-[var(--attention)]"
          : ["needs_review", "accept", "unresolved", "evidence_supported", "retrieved"].includes(state)
            ? "border-[var(--line)] bg-[var(--accent-soft)] text-[var(--accent)]"
          : ["rejected", "blocked", "failed", "interrupted", "revoked", "reject", "withdrawn", "dependency_invalidated", "evidence_not_supported"].includes(state)
            ? "border-[var(--line)] bg-[var(--del-bg)] text-[var(--del)]"
            : "border-[var(--line)] bg-white text-[var(--ink-2)]",
        className,
      )}
    >
      {children ?? value}
    </span>
  );
}
