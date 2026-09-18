import React from "react";
import { Collapsible, CollapsibleTrigger, CollapsibleContent } from "./collapsible";
import { Button } from "./button";
import { ChevronRight } from "./icon";
import { cn } from "@/lib/utils";

/** Shared shadcn composition for optional evidence and technical detail. */
export function Disclosure(props: React.ComponentProps<typeof Collapsible>) {
  return <Collapsible data-slot="collapsible" {...props} />;
}
export function DisclosureTrigger({children, className, ...props}: React.ComponentProps<typeof CollapsibleTrigger>) {
  return <CollapsibleTrigger asChild {...props}><Button variant="ghost" size="content" data-slot="collapsible-trigger" className={cn("group flex w-full items-center justify-between gap-3 py-3 text-left", className)}><span>{children}</span><ChevronRight className="size-4 shrink-0 transition-transform group-data-[state=open]:rotate-90" /></Button></CollapsibleTrigger>;
}
export function DisclosureContent({className, ...props}: React.ComponentProps<typeof CollapsibleContent>) {
  return <CollapsibleContent forceMount data-slot="collapsible-content" className={cn("data-[state=closed]:hidden", className)} {...props} />;
}
