import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const variants = cva(
  "inline-flex h-10 items-center justify-center gap-2 rounded-sm px-4 font-['DM_Sans'] text-[13px] font-semibold tracking-[-0.01em] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0E6675] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-45",
  {
    variants: {
      variant: {
        default: "border border-[#181A20] bg-[#181A20] text-white hover:bg-[#2A2D33]",
        outline: "border border-[#CBD1D5] bg-white text-[#272A30] hover:bg-[#F6F7F7]",
        request: "border border-[#0E6675] bg-white text-[#0E6675] hover:bg-[#F1F7F8]",
        ghost: "text-[#555B66] hover:bg-[#F6F7F7] hover:text-[#181A20]",
        danger: "border border-[#DAB8B4] bg-white text-[#963F38] hover:bg-[#FBF4F3]",
        approve: "border border-[#0E6675] bg-[#0E6675] text-white hover:bg-[#0A5360]",
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
