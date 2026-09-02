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
        "inline-flex items-center rounded-full border px-2 py-0.5 text-[11px] font-medium capitalize",
        state === "admitted"
          ? "border-emerald-200 bg-emerald-50 text-emerald-700"
          : state === "rejected" || state === "blocked"
            ? "border-red-200 bg-red-50 text-red-700"
            : "border-slate-200 bg-slate-100 text-slate-700",
        className,
      )}
    >
      {value}
    </span>
  );
}
