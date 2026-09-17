import React from "react";
import { DialogContent } from "./dialog";

/** Shared shadcn dialog surface for owner decisions and recorded handoffs. */
export function ModalSurface({children, ...props}: React.ComponentProps<typeof DialogContent>) {
  return <DialogContent {...props} showCloseButton={false} className="confirmationDialog">{children}</DialogContent>;
}
