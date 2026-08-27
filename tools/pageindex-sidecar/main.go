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
	"strings"
	"time"

	pageindex "github.com/neurondb/pageindex/pkg/pageindex"
)

const schema = "proofpress/pageindex-sidecar/v1"

type Source struct {
	SourceID             string `json:"source_id"`
	Path                 string `json:"path"`
	URI                  string `json:"uri"`
	ContentDigest        string `json:"content_digest"`
	MediaType            string `json:"media_type"`
	RepresentationDigest string `json:"representation_digest,omitempty"`
	TransformDigest      string `json:"transform_digest,omitempty"`
	PageCount            int    `json:"page_count,omitempty"`
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
	key := sha256Text(source.ContentDigest + "\n" + config)
	return filepath.Join(dir, strings.TrimPrefix(key, "sha256:")+".json")
}
func loadOrBuild(req Request, source Source) (*pageindex.Document, bool, error) {
	path := cachePath(req, source)
	if raw, err := os.ReadFile(path); err == nil {
		var doc pageindex.Document
		if err := json.Unmarshal(raw, &doc); err == nil {
			return &doc, true, nil
		}
		return nil, false, fmt.Errorf("invalid cached tree for %s", source.URI)
	}
	if source.MediaType != "application/pdf" {
		return nil, false, fmt.Errorf("PageIndex sidecar v1 supports application/pdf only: %s", source.URI)
	}
	doc, err := pageindex.BuildFromPDF(source.Path,
		pageindex.WithModel(runtimeModel(req.Config)), pageindex.WithAddNodeID(true),
		pageindex.WithAddNodeText(true), pageindex.WithAddNodeSummary(false),
		pageindex.WithAddDocDescription(false), pageindex.WithTOCCheckPages(1),
		pageindex.WithMaxPagesPerNode(1), pageindex.WithMaxTokensPerNode(2500))
	if err != nil {
		return nil, false, err
	}
	raw, err := json.Marshal(doc)
	if err != nil {
		return nil, false, err
	}
	if err := os.MkdirAll(filepath.Dir(path), 0700); err != nil {
		return nil, false, err
	}
	if err := os.WriteFile(path, raw, 0600); err != nil {
		return nil, false, err
	}
	return doc, false, nil
}
func receipt(source Source, node *pageindex.Node, req Request) (Envelope, error) {
	quote := strings.TrimSpace(node.Text)
	if quote == "" || node.NodeID == "" || node.StartIndex < 1 || node.EndIndex < node.StartIndex {
		return Envelope{}, fmt.Errorf("selected node cannot produce a bound section/page locator")
	}
	var out Envelope
	out.SchemaVersion = "proofpress/retrieval-evidence/v1"
	out.Source.URI, out.Source.ContentDigest, out.Source.MediaType = source.URI, source.ContentDigest, source.MediaType
	out.Source.RepresentationDigest, out.Source.TransformDigest = source.RepresentationDigest, source.TransformDigest
	out.Evidence.Quote = quote
	out.Evidence.Locator = map[string]any{"kind": "section_span", "section_id": node.NodeID,
		"section_digest": sha256Text(node.Title + "\n" + node.Text), "page_start": node.StartIndex, "page_end": node.EndIndex}
	out.Retrieval.Adapter, out.Retrieval.Version, out.Retrieval.Query = "proofpress.pageindex", "1", req.Query
	out.Retrieval.ConfigDigest, _ = req.Config["config_digest"].(string)
	out.Retrieval.SelectionReason = "PageIndex tree search selected section " + node.NodeID
	if out.Retrieval.ConfigDigest == "" {
		return Envelope{}, fmt.Errorf("missing config_digest")
	}
	return out, nil
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
	var receipts []Envelope
	var bytes int64
	cacheHits := 0
	for _, source := range req.Sources {
		actual, err := sha256File(source.Path)
		if err != nil || actual != source.ContentDigest {
			fmt.Fprintln(os.Stderr, "source custody check failed:", source.URI)
			os.Exit(3)
		}
		info, _ := os.Stat(source.Path)
		if info != nil {
			bytes += info.Size()
		}
		doc, cacheHit, err := loadOrBuild(req, source)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(4)
		}
		if cacheHit {
			cacheHits++
		}
		nodes, err := pageindex.TreeSearch(doc, req.Query, pageindex.WithSearchModel(runtimeModel(req.Config)), pageindex.WithMaxNodes(req.MaxResults-len(receipts)))
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(5)
		}
		for _, node := range nodes {
			item, err := receipt(source, node, req)
			if err != nil {
				fmt.Fprintln(os.Stderr, err)
				os.Exit(6)
			}
			receipts = append(receipts, item)
			if len(receipts) == req.MaxResults {
				break
			}
		}
		if len(receipts) == req.MaxResults {
			break
		}
	}
	json.NewEncoder(os.Stdout).Encode(map[string]any{"schema_version": schema, "fallback_used": false,
		"sidecar": map[string]any{"adapter": "proofpress.pageindex", "version": "1"}, "receipts": receipts,
		"telemetry": map[string]any{"latency_ms": time.Since(started).Milliseconds(), "source_bytes": bytes, "cost_usd": nil,
			"index_cache_hits": cacheHits, "index_cache_misses": len(req.Sources) - cacheHits,
			"fallback_used": false}})
}
