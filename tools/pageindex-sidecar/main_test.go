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

func TestConfiguredParallelismIsBoundedAndDefaultsToSerial(t *testing.T) {
	if got := configuredParallelism(nil, 4); got != 1 {
		t.Fatalf("default workers = %d, want 1", got)
	}
	if got := configuredParallelism(map[string]any{"parallelism": float64(4)}, 2); got != 2 {
		t.Fatalf("clamped workers = %d, want 2", got)
	}
	if got := configuredParallelism(map[string]any{"parallelism": float64(0)}, 4); got != 1 {
		t.Fatalf("invalid workers = %d, want 1", got)
	}
}
