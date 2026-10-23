import React from "react";
import { Button } from "./ui/button";
import { Disclosure, DisclosureContent, DisclosureTrigger } from "./ui/disclosure";
import "./provider-key-storage.css";

export type LocalServerSetup = {database: string; port: number};

function shellQuote(value: string) {
  return "'" + value.replaceAll("'", "'\\''") + "'";
}

export function localKeyStorageCommands(server: LocalServerSetup, existingCredential: boolean) {
  const initialize = existingCredential ? "" : `umask 077
mkdir -p "$HOME/.local/share/proofpress"
python3 - <<'PY'
import base64
import os
from pathlib import Path

key_file = Path.home() / ".local/share/proofpress/provider-key-encryption.key"
try:
    with key_file.open("x", encoding="ascii") as output:
        output.write(base64.urlsafe_b64encode(os.urandom(32)).decode("ascii") + "\\n")
except FileExistsError:
    pass
PY

`;
  return `${initialize}export PROOFPRESS_SECRET_ENCRYPTION_KEY="$(cat "$HOME/.local/share/proofpress/provider-key-encryption.key")"
proofpress hosted --database ${shellQuote(server.database)} \\
  serve --host 127.0.0.1 --port ${server.port}`;
}

export function ProviderKeyStorage({server, existingCredential, onCheck}: {
  server?: LocalServerSetup; existingCredential: boolean; onCheck: () => Promise<boolean>;
}) {
  const [open, setOpen] = React.useState(false);
  const [checking, setChecking] = React.useState(false);
  const [status, setStatus] = React.useState("");
  const [copied, setCopied] = React.useState(false);
  const commands = server ? localKeyStorageCommands(server, existingCredential) : "";
  async function copy() {
    try {
      await navigator.clipboard.writeText(commands);
      setCopied(true); setStatus("Copied. Run in the Terminal tab that starts Proofpress.");
    } catch {
      setCopied(false); setOpen(true); setStatus("Copy unavailable. Select and copy the commands below.");
    }
  }
  async function check() {
    setChecking(true); setStatus("");
    try {
      const ready = await onCheck();
      if (!ready) setStatus("Encrypted storage is still unavailable. Restart Proofpress with its encryption key loaded, then check again.");
    } catch {
      setStatus("Could not reach Proofpress. Finish restarting the server, then check again.");
    } finally { setChecking(false); }
  }
  return <section className="providerStorageSetup" aria-labelledby="providerStorageTitle">
    <h3 id="providerStorageTitle">{existingCredential ? "Restore access to your saved API key" : server ? "Set up local encrypted storage" : "Encrypted storage needs setup"}</h3>
    <p>API key entry is paused until this server can encrypt provider credentials.</p>
    {server ? <>
      <ol className="providerStorageSteps">
        <li>Stop the Proofpress server with <kbd>Ctrl-C</kbd> in its Terminal tab.</li>
        <li>{existingCredential ? <>Restore your <strong>original encryption key</strong> to <code>~/.local/share/proofpress/provider-key-encryption.key</code>. If it lives elsewhere, adjust the restart command to load that file. Do not generate a replacement.</> : <>Run the setup commands there. They create a private encryption key file once and restart this database on port {server.port}.</>}</li>
        <li>Keep that tab running, then check storage again here to continue entering your provider key.</li>
      </ol>
      <Disclosure open={open} onOpenChange={setOpen}>
        <DisclosureTrigger>{existingCredential ? "Terminal restart commands" : "Terminal setup commands"}</DisclosureTrigger>
        <DisclosureContent><pre className="providerStorageCommands" tabIndex={0} aria-label="Encrypted storage terminal commands"><code>{commands}</code></pre></DisclosureContent>
      </Disclosure>
      <div className="providerStorageActions"><Button type="button" variant="outline" onClick={copy}>{copied ? "Copied" : existingCredential ? "Copy restart commands" : "Copy setup commands"}</Button><Button type="button" variant="outline" disabled={checking} onClick={check}>{checking ? "Checking…" : "Check storage again"}</Button></div>
      <p className="providerStorageFootnote">Use the same encryption file every time you start Proofpress. Keep a protected backup outside Git. This sets up storage; you choose your provider and authorize AI processing when saving below.</p>
    </> : <>
      <p>Your server operator needs to configure <code>PROOFPRESS_SECRET_ENCRYPTION_KEY</code> and restart the service. Existing saved keys require the original encryption key.</p>
      <div className="providerStorageActions"><Button type="button" variant="outline" disabled={checking} onClick={check}>{checking ? "Checking…" : "Check storage again"}</Button></div>
    </>}
    <p className="providerStorageStatus" role="status" aria-live="polite">{status}</p>
  </section>;
}
