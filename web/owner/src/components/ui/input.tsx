import * as React from "react";
import { cn } from "@/lib/utils";

export function Input({ className, ...props }: React.ComponentProps<"input">) {
  return <input data-slot="input" className={cn("flex h-10 w-full min-w-0 rounded-md border border-[var(--line)] bg-[var(--paper)] px-3 text-sm text-[var(--ink)] placeholder:text-[var(--ink-3)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)] disabled:cursor-not-allowed disabled:opacity-50", className)} {...props} />;
}
