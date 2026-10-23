import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { localKeyStorageCommands, ProviderKeyStorage } from "./provider-key-storage";

describe("provider key storage recovery", () => {
  it("uses the actual instance and shell-quotes database paths", () => {
    const commands = localKeyStorageCommands({database:"/tmp/Bing's research; notes/workspace.db",port:8444},false);
    expect(commands).toContain("--database '/tmp/Bing'\\''s research; notes/workspace.db'");
    expect(commands).toContain("--port 8444");
    expect(commands).toContain('key_file.open("x"');
    expect(commands).toContain('PROOFPRESS_SECRET_ENCRYPTION_KEY="$(cat ');
  });
  it("never offers key generation when a provider credential already exists", () => {
    const commands = localKeyStorageCommands({database:"/tmp/workspace.db",port:7334},true);
    expect(commands).not.toContain("os.urandom");
    expect(commands).toContain("serve --host 127.0.0.1");
    const html=renderToStaticMarkup(<ProviderKeyStorage server={{database:"/tmp/workspace.db",port:7334}} existingCredential onCheck={async()=>false} />);
    expect(html).toContain("Restore access to your saved API key");
    expect(html).toContain("Do not generate a replacement");
  });
  it("keeps remote recovery free of local paths and terminal commands", () => {
    const html=renderToStaticMarkup(<ProviderKeyStorage existingCredential={false} onCheck={async()=>false} />);
    expect(html).toContain("Your server operator");
    expect(html).toContain("Check storage again");
    expect(html).not.toContain("Copy setup commands");
    expect(html).not.toContain(".local/share");
  });
});
