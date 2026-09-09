import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const variants = cva(
  "inline-flex items-center justify-center gap-2 rounded-sm font-['DM_Sans'] font-semibold tracking-[-0.01em] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-45",
  {
    variants: {
      variant: {
        default: "border border-[var(--ink)] bg-[var(--ink)] text-white hover:bg-[#2A2D33]",
        outline: "border border-[var(--line)] bg-white text-[var(--ink)] hover:bg-[var(--wash)]",
        request: "border border-[var(--accent)] bg-white text-[var(--accent)] hover:bg-[var(--accent-soft)]",
        accent: "border border-[var(--accent)] bg-[var(--accent)] text-white hover:bg-[var(--accent-strong)]",
        ghost: "text-[var(--ink-2)] hover:bg-[var(--wash)] hover:text-[var(--ink)]",
        danger: "border border-[var(--del)] bg-white text-[var(--del)] hover:bg-[var(--del-bg)]",
        approve: "border border-[var(--accent)] bg-[var(--accent)] text-white hover:bg-[var(--accent-strong)]",
      },
      size: {
        default: "h-11 px-4 text-[13px]",
        sm: "h-8 px-3 text-[12px]",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
);
export interface ButtonProps
  extends
    React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof variants> {
  ref?: React.Ref<HTMLButtonElement>;
}
export function Button({ className, variant, size, ...props }: ButtonProps) {
  return <button className={cn(variants({ variant, size }), className)} {...props} />;
}
