import * as React from "react";
import { cn } from "@/lib/utils";

export function Card({className,...props}:React.HTMLAttributes<HTMLDivElement>){return <div className={cn("rounded-xl border border-[var(--line)] bg-white text-[var(--ink)] shadow-[0_1px_2px_rgba(24,26,32,.04)]",className)} {...props}/>}
export function CardHeader({className,...props}:React.HTMLAttributes<HTMLDivElement>){return <div className={cn("flex flex-col gap-1.5 p-6",className)} {...props}/>}
export function CardTitle({className,...props}:React.HTMLAttributes<HTMLHeadingElement>){return <h3 className={cn("font-['DM_Sans'] text-base font-semibold tracking-[-.015em]",className)} {...props}/>}
export function CardDescription({className,...props}:React.HTMLAttributes<HTMLParagraphElement>){return <p className={cn("text-sm leading-6 text-[var(--ink-2)]",className)} {...props}/>}
export function CardContent({className,...props}:React.HTMLAttributes<HTMLDivElement>){return <div data-slot="card-content" className={cn("p-6 pt-0",className)} {...props}/>}
