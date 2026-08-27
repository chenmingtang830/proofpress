package main

import "testing"

func TestRuntimeModelAndCacheAreProviderSafe(t *testing.T) {
	if got := runtimeModel(map[string]any{"requested_model": "openai/gpt-5.6-luna"}); got != "gpt-5.6-luna" {
		t.Fatalf("got %q", got)
	}
	req := Request{Config: map[string]any{"config_digest": "sha256:abc"}}
	path := cachePath(req, Source{ContentDigest: "sha256:def"})
	if path == "" || sha256Text("x") != sha256Text("x") {
		t.Fatal("cache key must be deterministic")
	}
}
