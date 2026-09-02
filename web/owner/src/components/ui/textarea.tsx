// Adapted from shadcn/ui's New York Textarea registry component.
import * as React from "react";
import { cn } from "@/lib/utils";

const Textarea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<"textarea">>(
  ({ className, ...props }, ref) => (
    <textarea ref={ref} className={cn(
      "flex min-h-[60px] w-full rounded-md border border-[#E3E1D9] bg-transparent px-3 py-2 text-sm placeholder:text-[#5A5D6B] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#0E5E6F] disabled:cursor-not-allowed disabled:opacity-50",
      className,
    )} {...props} />
  ),
);
Textarea.displayName = "Textarea";
export { Textarea };
