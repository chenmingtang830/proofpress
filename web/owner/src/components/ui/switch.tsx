import React from "react";
import { cn } from "@/lib/utils";

type SwitchProps = Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, "onChange"> & {
  checked: boolean;
  onCheckedChange: (checked: boolean) => void;
};

export function Switch({checked, onCheckedChange, className, disabled, ...props}: SwitchProps) {
  return <button {...props} type="button" role="switch" aria-checked={checked} disabled={disabled}
    data-slot="switch" className={cn("uiSwitch",className)}
    onClick={()=>onCheckedChange(!checked)}><span aria-hidden="true" /></button>;
}
