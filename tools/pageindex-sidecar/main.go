// pageindex-sidecar is a local JSON-lines boundary around PageIndex.
// It never receives credentials in its protocol and never contacts a hosted
// retrieval service. PageIndex itself reads OPENAI_API_KEY only when invoked.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"sync"
	"time"

	pageindex "github.com/neurondb/pageindex/pkg/pageindex"
)

const schema = "proofpress/pageindex-sidecar/v1"

type Source struct {
	SourceID             string            `json:"source_id"`
	Path                 string            `json:"path"`
	URI                  string            `json:"uri"`
	ContentDigest        string            `json:"content_digest"`
	MediaType            string            `json:"media_type"`
	RepresentationDigest string            `json:"representation_digest,omitempty"`
	TransformDigest      string            `json:"transform_digest,omitempty"`
	PageCount            int               `json:"page_count,omitempty"`
	PathDigest           string            `json:"path_digest,omitempty"`
	RepresentationKind   string            `json:"representation_kind,omitempty"`
	LocatorMap           []LocatorMapEntry `json:"locator_map,omitempty"`
}
type LocatorMapEntry struct {
	Line          int    `json:"line"`
	SectionID     string `json:"section_id"`
	SectionDigest string `json:"section_digest"`
	PageStart     int    `json:"page_start"`
	PageEnd       int    `json:"page_end"`
}
type Request struct {
	SchemaVersion string         `json:"schema_version"`
	Query         string         `json:"query"`
	Sources       []Source       `json:"sources"`
	Config        map[string]any `json:"config"`
	MaxResults    int            `json:"max_results"`
	CacheDir      string         `json:"cache_dir,omitempty"`
}
type Envelope struct {
	SchemaVersion string `json:"schema_version"`
	Source        struct {
		URI                  string `json:"uri"`
		ContentDigest        string `json:"content_digest"`
		MediaType            string `json:"media_type"`
		RepresentationDigest string `json:"representation_digest,omitempty"`
		TransformDigest      string `json:"transform_digest,omitempty"`
	} `json:"source"`
	Evidence struct {
		Quote   string         `json:"quote"`
		Locator map[string]any `json:"locator"`
	} `json:"evidence"`
	Retrieval struct {
		Adapter         string `json:"adapter"`
		Version         string `json:"version"`
		Query           string `json:"query"`
		ConfigDigest    string `json:"config_digest"`
		SelectionReason string `json:"selection_reason"`
	} `json:"retrieval"`
}

func sha256File(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()
	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", err
	}
	return "sha256:" + hex.EncodeToString(h.Sum(nil)), nil
}
func sha256Text(text string) string {
	h := sha256.Sum256([]byte(text))
	return "sha256:" + hex.EncodeToString(h[:])
}
func runtimeModel(config map[string]any) string {
	value, _ := config["requested_model"].(string)
	return strings.TrimPrefix(value, "openai/")
}
func cachePath(req Request, source Source) string {
	dir := req.CacheDir
	if dir == "" {
		dir = ".proofpress/pageindex-cache"
	}
	config, _ := req.Config["config_digest"].(string)
	identity := source.RepresentationDigest
	if identity == "" {
		identity = source.ContentDigest
	}
	key := sha256Text(identity + "\n" + config)
	return filepath.Join(dir, strings.TrimPrefix(key, "sha256:")+".json")
}
func retryOperation[T any](maxRetries int, operation func() (T, error)) (T, int, error) {
	var zero T
	var last error
	for attempt := 0; attempt <= maxRetries; attempt++ {
		value, err := operation()
		if err == nil {
			return value, attempt, nil
		}
		last = err
		if attempt < maxRetries {
			time.Sleep(time.Duration(attempt+1) * 250 * time.Millisecond)
		}
	}
	return zero, maxRetries, last
}

func loadOrBuild(req Request, source Source) (*pageindex.Document, bool, int, error) {
	path := cachePath(req, source)
	if raw, err := os.ReadFile(path); err == nil {
		var doc pageindex.Document
		if err := json.Unmarshal(raw, &doc); err == nil {
			return &doc, true, 0, nil
		}
		return nil, false, 0, fmt.Errorf("invalid cached tree for %s", source.URI)
	}
	var doc *pageindex.Document
	var err error
	options := []pageindex.Option{pageindex.WithModel(runtimeModel(req.Config)), pageindex.WithAddNodeID(true),
		pageindex.WithAddNodeText(true), pageindex.WithAddNodeSummary(false),
		pageindex.WithAddDocDescription(false)}
	build := func() (*pageindex.Document, error) {
		if source.RepresentationKind == "canonical_markdown" {
			if source.RepresentationDigest == "" || len(source.LocatorMap) == 0 {
				return nil, fmt.Errorf("canonical representation requires digest and locator map: %s", source.URI)
			}
			return pageindex.BuildFromMarkdown(source.Path, options...)
		} else if source.MediaType == "application/pdf" {
			return pageindex.BuildFromPDF(source.Path, append(options,
				pageindex.WithTOCCheckPages(1), pageindex.WithMaxPagesPerNode(1),
				pageindex.WithMaxTokensPerNode(2500))...)
		}
		return nil, fmt.Errorf("unsupported retrieval representation for %s", source.URI)
	}
	doc, retries, err := retryOperation(2, build)
	if err != nil {
		return nil, false, retries, err
	}
	raw, err := json.Marshal(doc)
	if err != nil {
		return nil, false, retries, err
	}
	if err := os.MkdirAll(filepath.Dir(path), 0700); err != nil {
		return nil, false, retries, err
	}
	if err := os.WriteFile(path, raw, 0600); err != nil {
		return nil, false, retries, err
	}
	return doc, false, retries, nil
}
func receipt(source Source, node *pageindex.Node, req Request) (Envelope, error) {
	quote := strings.TrimSpace(node.Text)
	if quote == "" || node.NodeID == "" {
		return Envelope{}, fmt.Errorf("selected node cannot produce a bound section/page locator")
	}
	var out Envelope
	out.SchemaVersion = "proofpress/retrieval-evidence/v1"
	out.Source.URI, out.Source.ContentDigest, out.Source.MediaType = source.URI, source.ContentDigest, source.MediaType
	out.Source.RepresentationDigest, out.Source.TransformDigest = source.RepresentationDigest, source.TransformDigest
	out.Evidence.Quote = quote
	if source.RepresentationKind == "canonical_markdown" {
		var mapped *LocatorMapEntry
		for index := range source.LocatorMap {
			if source.LocatorMap[index].Line <= node.LineNum && (mapped == nil || source.LocatorMap[index].Line > mapped.Line) {
				mapped = &source.LocatorMap[index]
			}
		}
		if mapped == nil || mapped.SectionID == "" || mapped.PageStart < 1 || mapped.PageEnd < mapped.PageStart {
			return Envelope{}, fmt.Errorf("selected canonical node cannot map to source locator")
		}
		out.Evidence.Locator = map[string]any{"kind": "section_span", "section_id": mapped.SectionID,
			"section_digest": mapped.SectionDigest, "page_start": mapped.PageStart, "page_end": mapped.PageEnd}
	} else {
		if node.StartIndex < 1 || node.EndIndex < node.StartIndex {
			return Envelope{}, fmt.Errorf("selected PDF node cannot produce a page locator")
		}
		out.Evidence.Locator = map[string]any{"kind": "section_span", "section_id": node.NodeID,
			"section_digest": sha256Text(node.Title + "\n" + node.Text), "page_start": node.StartIndex, "page_end": node.EndIndex}
	}
	out.Retrieval.Adapter, out.Retrieval.Version, out.Retrieval.Query = "proofpress.pageindex", "1", req.Query
	out.Retrieval.ConfigDigest, _ = req.Config["config_digest"].(string)
	out.Retrieval.SelectionReason = "PageIndex tree search selected section " + node.NodeID
	if out.Retrieval.ConfigDigest == "" {
		return Envelope{}, fmt.Errorf("missing config_digest")
	}
	return out, nil
}

func configuredParallelism(config map[string]any, sourceCount int) int {
	if sourceCount < 2 {
		return 1
	}
	workers := 1
	if value, ok := config["parallelism"].(float64); ok && value >= 1 {
		workers = int(value)
	}
	if workers > sourceCount {
		workers = sourceCount
	}
	return workers
}

func configuredMaxNodesPerSource(config map[string]any, remaining int) int {
	limit := remaining
	if value, ok := config["max_nodes_per_source"].(float64); ok && value >= 1 && int(value) < limit {
		limit = int(value)
	}
	if limit < 1 {
		return 1
	}
	return limit
}

type sourceResult struct {
	index        int
	source       Source
	doc          *pageindex.Document
	receipts     []Envelope
	bytes        int64
	cacheHit     bool
	buildRetries int
	err          error
}

func loadSource(req Request, index int, source Source) sourceResult {
	result := sourceResult{index: index, source: source}
	actual, err := sha256File(source.Path)
	expected := source.ContentDigest
	if source.PathDigest != "" {
		expected = source.PathDigest
	}
	if err != nil || actual != expected {
		result.err = fmt.Errorf("source custody check failed: %s", source.URI)
		return result
	}
	if info, statErr := os.Stat(source.Path); statErr == nil {
		result.bytes = info.Size()
	}
	doc, cacheHit, buildRetries, err := loadOrBuild(req, source)
	if err != nil {
		result.err = err
		return result
	}
	result.cacheHit = cacheHit
	result.buildRetries = buildRetries
	result.doc = doc
	return result
}

func searchSource(req Request, result sourceResult, maxNodes int) sourceResult {
	if result.err != nil || result.doc == nil {
		return result
	}
	nodes, err := pageindex.TreeSearch(result.doc, req.Query, pageindex.WithSearchModel(runtimeModel(req.Config)), pageindex.WithMaxNodes(maxNodes))
	if err != nil {
		result.err = err
		return result
	}
	for _, node := range nodes {
		item, receiptErr := receipt(result.source, node, req)
		if receiptErr != nil {
			result.err = receiptErr
			return result
		}
		result.receipts = append(result.receipts, item)
	}
	return result
}

func processSource(req Request, index int, source Source, maxNodes int) sourceResult {
	return searchSource(req, loadSource(req, index, source), maxNodes)
}

func accountLoadedResults(results []sourceResult) (int64, int, int, error) {
	var bytes int64
	cacheHits := 0
	buildRetries := 0
	for _, result := range results {
		if result.err != nil {
			return 0, 0, 0, result.err
		}
		bytes += result.bytes
		if result.cacheHit {
			cacheHits++
		}
		buildRetries += result.buildRetries
	}
	return bytes, cacheHits, buildRetries, nil
}

func main() {
	started := time.Now()
	var req Request
	if err := json.NewDecoder(os.Stdin).Decode(&req); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	if req.SchemaVersion != schema || strings.TrimSpace(req.Query) == "" || req.MaxResults < 1 || len(req.Sources) == 0 {
		fmt.Fprintln(os.Stderr, "invalid PageIndex sidecar request")
		os.Exit(2)
	}
	receipts := make([]Envelope, 0)
	var bytes int64
	cacheHits := 0
	buildRetries := 0
	workers := configuredParallelism(req.Config, len(req.Sources))
	if workers == 1 {
		// Preserve the original lazy, manifest-ordered behavior by default.
		for index, source := range req.Sources {
			result := processSource(req, index, source, configuredMaxNodesPerSource(req.Config, req.MaxResults-len(receipts)))
			if result.err != nil {
				fmt.Fprintln(os.Stderr, result.err)
				os.Exit(4)
			}
			bytes += result.bytes
			if result.cacheHit {
				cacheHits++
			}
			buildRetries += result.buildRetries
			for _, item := range result.receipts {
				receipts = append(receipts, item)
				if len(receipts) == req.MaxResults {
					break
				}
			}
			if len(receipts) == req.MaxResults {
				break
			}
		}
	} else {
		// Parallel mode evaluates every requested source, then restores manifest
		// order before applying max_results. This keeps output replayable while
		// allowing independent cold builds/searches to overlap.
		results := make([]sourceResult, len(req.Sources))
		jobs := make(chan int)
		var wg sync.WaitGroup
		for worker := 0; worker < workers; worker++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for index := range jobs {
					// Parallel mode overlaps only custody checks and cold tree
					// construction. Search remains manifest-ordered below, so
					// max_results and receipt ordering are unchanged.
					results[index] = loadSource(req, index, req.Sources[index])
				}
			}()
		}
		for index := range req.Sources {
			jobs <- index
		}
		close(jobs)
		wg.Wait()
		sort.Slice(results, func(i, j int) bool { return results[i].index < results[j].index })
		// All requested sources have already crossed custody and load/build above.
		// Account for every result before search applies max_results; otherwise a
		// receipt-saturated early break misreports trailing cache hits as misses.
		loadedBytes, loadedCacheHits, loadedBuildRetries, loadErr := accountLoadedResults(results)
		if loadErr != nil {
			fmt.Fprintln(os.Stderr, loadErr)
			os.Exit(4)
		}
		bytes += loadedBytes
		cacheHits += loadedCacheHits
		buildRetries += loadedBuildRetries
		for _, result := range results {
			searched := searchSource(req, result, configuredMaxNodesPerSource(req.Config, req.MaxResults-len(receipts)))
			if searched.err != nil {
				fmt.Fprintln(os.Stderr, searched.err)
				os.Exit(5)
			}
			for _, item := range searched.receipts {
				if len(receipts) == req.MaxResults {
					break
				}
				receipts = append(receipts, item)
			}
			if len(receipts) == req.MaxResults {
				break
			}
		}
	}
	json.NewEncoder(os.Stdout).Encode(map[string]any{"schema_version": schema, "fallback_used": false,
		"sidecar": map[string]any{"adapter": "proofpress.pageindex", "version": "1"}, "receipts": receipts,
		"telemetry": map[string]any{"latency_ms": time.Since(started).Milliseconds(), "source_bytes": bytes, "cost_usd": nil,
			"index_cache_hits": cacheHits, "index_cache_misses": len(req.Sources) - cacheHits,
			"source_build_retries": buildRetries,
			"fallback_used":        false}})
}
