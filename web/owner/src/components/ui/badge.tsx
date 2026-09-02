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
        state === "admitted"
          ? "border-[#C6DFC9] bg-[#E7F2EA] text-[#2E7D4F]"
          : state === "rejected" || state === "blocked"
            ? "border-[#E9C9C5] bg-[#F7E9E7] text-[#B4453A]"
            : "border-[#E3E1D9] bg-[#F1EFE8] text-[#5A5D6B]",
        className,
      )}
    >
      {value}
    </span>
  );
}
