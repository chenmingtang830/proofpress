import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const variants = cva(
  "inline-flex h-9 items-center justify-center gap-2 rounded-md px-3 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#5FB3C4] disabled:pointer-events-none disabled:opacity-45",
  {
    variants: {
      variant: {
        default: "bg-[#0E5E6F] text-white hover:bg-[#0A4B59]",
        outline: "border border-[#E3E1D9] bg-white hover:bg-[#F1EFE8]",
        ghost: "hover:bg-[#F1EFE8]",
        danger: "border border-[#E9C9C5] bg-white text-[#B4453A] hover:bg-[#F7E9E7]",
        approve: "bg-[#2E7D4F] text-white hover:bg-[#256840]",
      },
    },
    defaultVariants: { variant: "default" },
  },
);
export interface ButtonProps
  extends
    React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof variants> {}
export function Button({ className, variant, ...props }: ButtonProps) {
  return <button className={cn(variants({ variant }), className)} {...props} />;
}
