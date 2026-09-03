import { cn } from "@/lib/utils";
export function Badge({
  state,
  className,
}: {
  state: string;
  className?: string;
}) {
  const value = state.replaceAll("_", " ");
  return (
    <span
      className={cn(
        "inline-flex h-6 shrink-0 items-center justify-center whitespace-nowrap rounded-full border px-2.5 text-[11px] leading-none font-medium capitalize",
        state === "admitted" || state === "active"
          ? "border-[var(--line)] bg-[var(--add-bg)] text-[var(--add)]"
          : state === "needs_revision"
            ? "border-[var(--revision)] bg-[var(--revision-bg)] text-[var(--revision)]"
          : state === "rejected" || state === "blocked" || state === "revoked"
            ? "border-[var(--line)] bg-[var(--del-bg)] text-[var(--del)]"
            : "border-[var(--line)] bg-[var(--wash)] text-[var(--ink-2)]",
        className,
      )}
    >
      {value}
    </span>
  );
}
