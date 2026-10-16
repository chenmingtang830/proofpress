import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const variants = cva(
  "inline-flex items-center justify-center gap-2 rounded-full font-['DM_Sans'] font-semibold tracking-[-0.01em] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-45",
  {
    variants: {
      variant: {
        default: "border border-[var(--accent)] bg-[var(--accent)] text-white hover:bg-[var(--accent-strong)]",
        outline: "border border-[var(--line)] bg-white text-[var(--ink)] hover:bg-[var(--wash)]",
        request: "border border-[var(--accent)] bg-white text-[var(--accent)] hover:bg-[var(--accent-soft)]",
        accent: "border border-[var(--accent)] bg-[var(--accent)] text-white hover:bg-[var(--accent-strong)]",
        ghost: "text-[var(--ink-2)] hover:bg-[var(--wash)] hover:text-[var(--ink)]",
        danger: "border border-[var(--del)] bg-white text-[var(--del)] hover:bg-[var(--del-bg)]",
        approve: "border border-[var(--accent)] bg-[var(--accent)] text-white hover:bg-[var(--accent-strong)]",
      },
      size: {
        content: "justify-start h-auto whitespace-normal p-0 text-left text-[13px]",
        default: "min-h-11 px-5 py-2.5 text-[14px]",
        sm: "min-h-9 px-4 py-2 text-[13px]",
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
  return <button data-slot="button" data-variant={variant || "default"} data-size={size || "default"} className={cn(variants({ variant, size }), className)} {...props} />;
}
