import * as React from "react";
import * as RadioGroupPrimitive from "@radix-ui/react-radio-group";
import { cn } from "@/lib/utils";

export const RadioGroup=RadioGroupPrimitive.Root;
export function RadioGroupItem({className,...props}:React.ComponentProps<typeof RadioGroupPrimitive.Item>){return <RadioGroupPrimitive.Item className={cn("grid size-4 shrink-0 place-items-center rounded-full border border-[var(--ink-3)] text-[var(--accent)] data-[state=checked]:border-[var(--accent)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)]",className)} {...props}><RadioGroupPrimitive.Indicator className="size-2 rounded-full bg-current"/></RadioGroupPrimitive.Item>}
