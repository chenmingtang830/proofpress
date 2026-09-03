import React from "react";
import * as Dialog from "@radix-ui/react-dialog";

/** Shared accessible surface for owner decisions and recorded handoffs. */
export function ModalSurface({children, ...props}: React.ComponentProps<typeof Dialog.Content>) {
  return <Dialog.Portal><Dialog.Overlay className="confirmationOverlay" /><Dialog.Content {...props} className="confirmationDialog">{children}</Dialog.Content></Dialog.Portal>;
}
