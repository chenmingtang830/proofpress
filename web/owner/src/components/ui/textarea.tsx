// Adapted from shadcn/ui's New York Textarea registry component.
import * as React from "react";
import { cn } from "@/lib/utils";

const Textarea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<"textarea">>(
  ({ className, ...props }, ref) => (
    <textarea ref={ref} data-slot="textarea" className={cn(
      "flex min-h-[100px] w-full rounded-xl border border-[var(--control-border)] bg-[var(--paper)] px-4 py-3 text-sm text-[var(--ink)] placeholder:text-[var(--ink-3)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)] disabled:cursor-not-allowed disabled:opacity-50",
      className,
    )} {...props} />
  ),
);
Textarea.displayName = "Textarea";
export { Textarea };
