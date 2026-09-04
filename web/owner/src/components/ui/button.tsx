import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const variants = cva(
  "inline-flex h-11 items-center justify-center gap-2 rounded-sm px-4 font-['DM_Sans'] text-[13px] font-semibold tracking-[-0.01em] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-45",
  {
    variants: {
      variant: {
        default: "border border-[var(--ink)] bg-[var(--ink)] text-white hover:bg-[#2A2D33]",
        outline: "border border-[var(--line)] bg-white text-[var(--ink)] hover:bg-[var(--wash)]",
        request: "border border-[var(--accent)] bg-white text-[var(--accent)] hover:bg-[var(--accent-soft)]",
        ghost: "text-[var(--ink-2)] hover:bg-[var(--wash)] hover:text-[var(--ink)]",
        danger: "border border-[var(--del)] bg-white text-[var(--del)] hover:bg-[var(--del-bg)]",
        approve: "border border-[var(--accent)] bg-[var(--accent)] text-white hover:bg-[var(--accent-strong)]",
      },
    },
    defaultVariants: { variant: "default" },
  },
);
export interface ButtonProps
  extends
    React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof variants> {
  ref?: React.Ref<HTMLButtonElement>;
}
export function Button({ className, variant, ...props }: ButtonProps) {
  return <button className={cn(variants({ variant }), className)} {...props} />;
}
