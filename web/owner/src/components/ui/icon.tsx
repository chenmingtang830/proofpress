import React from "react";
import { HugeiconsIcon } from "@hugeicons/react";
import { Activity01Icon, ArrowRight01Icon, BookOpen01Icon, Cancel01Icon, Home01Icon, Key01Icon, Shield01Icon, Tick02Icon } from "@hugeicons/core-free-icons";

const glyphs = {activity:Activity01Icon, arrowRight:ArrowRight01Icon, book:BookOpen01Icon, close:Cancel01Icon, home:Home01Icon, key:Key01Icon, shield:Shield01Icon, check:Tick02Icon};
type IconProps = Omit<React.ComponentProps<typeof HugeiconsIcon>, "icon" | "name">;
export function Icon({name, ...props}: IconProps & {name:keyof typeof glyphs}) {
  return <HugeiconsIcon icon={glyphs[name]} size={20} strokeWidth={1.6} color="currentColor" aria-hidden="true" {...props} />;
}
const named = (name:keyof typeof glyphs) => (props:IconProps) => <Icon name={name} {...props} />;
export const Activity = named("activity");
export const BookOpen = named("book");
export const Check = named("check");
export const ChevronRight = named("arrowRight");
export const Home = named("home");
export const KeyRound = named("key");
export const ShieldCheck = named("shield");
export const X = named("close");
