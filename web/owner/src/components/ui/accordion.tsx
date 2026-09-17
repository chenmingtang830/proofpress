import * as React from "react";
import * as AccordionPrimitive from "@radix-ui/react-accordion";
import { ChevronRight } from "./icon";
import { cn } from "@/lib/utils";

export const Accordion=AccordionPrimitive.Root;
export function AccordionItem({className,...props}:React.ComponentProps<typeof AccordionPrimitive.Item>){return <AccordionPrimitive.Item className={cn("border-b border-[var(--line)]",className)} {...props}/>}
export function AccordionTrigger({className,children,...props}:React.ComponentProps<typeof AccordionPrimitive.Trigger>){return <AccordionPrimitive.Header className="flex"><AccordionPrimitive.Trigger className={cn("group flex min-h-12 flex-1 items-center justify-between py-3 text-left text-sm font-semibold transition-colors hover:text-[var(--accent)]",className)} {...props}>{children}<ChevronRight className="ml-4 size-4 shrink-0 text-[var(--ink-3)] transition-transform group-data-[state=open]:rotate-90" /></AccordionPrimitive.Trigger></AccordionPrimitive.Header>}
export function AccordionContent({className,children,...props}:React.ComponentProps<typeof AccordionPrimitive.Content>){return <AccordionPrimitive.Content className="overflow-hidden text-sm data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down" {...props}><div className={cn("pb-5 leading-6 text-[var(--ink-2)]",className)}>{children}</div></AccordionPrimitive.Content>}
