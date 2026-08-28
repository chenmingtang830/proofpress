package main

import (
	"errors"
	"testing"

	pageindex "github.com/neurondb/pageindex/pkg/pageindex"
)

func TestRetryOperationAllowsExactlyTwoRetries(t *testing.T) {
	attempts := 0
	value, retries, err := retryOperation(2, func() (string, error) {
		attempts++
		if attempts < 3 {
			return "", errors.New("transient")
		}
		return "ok", nil
	})
	if err != nil || value != "ok" || retries != 2 || attempts != 3 {
		t.Fatalf("value=%q retries=%d attempts=%d err=%v", value, retries, attempts, err)
	}
}

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

func TestCanonicalMarkdownReceiptMapsBackToCatalogSection(t *testing.T) {
	source := Source{URI: "private://mail", ContentDigest: "sha256:source", MediaType: "application/mbox",
		RepresentationDigest: "sha256:representation", TransformDigest: "sha256:transform",
		RepresentationKind: "canonical_markdown", LocatorMap: []LocatorMapEntry{{
			Line: 3, SectionID: "sec_1", SectionDigest: "sha256:section", PageStart: 7, PageEnd: 7}}}
	req := Request{Query: "email", Config: map[string]any{"config_digest": "sha256:config"}}
	item, err := receipt(source, &pageindex.Node{Title: "Email", NodeID: "node_1", Text: "body", LineNum: 3}, req)
	if err != nil {
		t.Fatal(err)
	}
	if item.Evidence.Locator["section_id"] != "sec_1" || item.Evidence.Locator["page_start"] != 7 {
		t.Fatalf("unexpected locator: %#v", item.Evidence.Locator)
	}
	if item.Source.ContentDigest != "sha256:source" || item.Source.RepresentationDigest != "sha256:representation" {
		t.Fatalf("custody fields were not preserved: %#v", item.Source)
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

func TestConfiguredMaxNodesPerSourcePreventsFirstDocumentDominance(t *testing.T) {
	if got := configuredMaxNodesPerSource(nil, 20); got != 20 {
		t.Fatalf("default per-source limit = %d, want 20", got)
	}
	config := map[string]any{"max_nodes_per_source": float64(3)}
	if got := configuredMaxNodesPerSource(config, 20); got != 3 {
		t.Fatalf("configured per-source limit = %d, want 3", got)
	}
	if got := configuredMaxNodesPerSource(config, 2); got != 2 {
		t.Fatalf("remaining-result clamp = %d, want 2", got)
	}
}

func TestAccountLoadedResultsIncludesTrailingCacheHits(t *testing.T) {
	results := []sourceResult{
		{bytes: 10, cacheHit: true, buildRetries: 0},
		{bytes: 20, cacheHit: true, buildRetries: 1},
		{bytes: 30, cacheHit: true, buildRetries: 0},
	}
	bytes, cacheHits, buildRetries, err := accountLoadedResults(results)
	if err != nil {
		t.Fatal(err)
	}
	if bytes != 60 || cacheHits != 3 || buildRetries != 1 {
		t.Fatalf("bytes=%d cacheHits=%d buildRetries=%d", bytes, cacheHits, buildRetries)
	}
}
