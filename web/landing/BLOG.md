# Native blog import

Imports are explicit, local, and reviewable. They never publish, schedule polling, or change the original social post. The homepage shows the latest imported articles. Vite emits complete HTML article pages, canonical URLs, BlogPosting metadata, and a sitemap; reading requires no JavaScript.

## X article or post

```sh
npm --prefix web/landing run blog:import -- 'https://x.com/richardt830/status/2097453369535386089' --slug memory-is-not-enough
```

X retrieval uses the public **third-party FxTwitter API**, not the official authenticated X API. Availability is not guaranteed. Only richardt830 posts are accepted. Original body, styles, links, captions, publication dates, and available article images are retained; downloaded assets live in `public/blog-media`. Ordinary posts need an explicit `--title`. No credential is needed or read.

Reimporting an existing source is a no-op (and repairs a missing/stale `post-index.json`). The generated summary index keeps full article bodies out of the homepage JavaScript bundle. Use `--replace` to intentionally refresh a source without changing its slug. A slug collision with another source fails. Inspect the diff before replacing. New imports update `src/content/posts.json` only after retrieval succeeds; a failed asset download can leave unused local media, but does not replace the article collection.

## LinkedIn

```sh
npm --prefix web/landing run blog:import -- 'https://www.linkedin.com/pulse/YOUR-ARTICLE' --slug your-article
```

Direct import requires public Article/BlogPosting structured data with a substantial `articleBody`, author Richard Tang, and a publication date. Login walls, short excerpts, missing metadata, and redirects fail rather than silently publishing a preview. This route is fixture-tested, not verified against Richard's live LinkedIn article. Public structured data is not proof of completeness: always compare the local page to the original. This adapter imports text, not LinkedIn rich media.

If LinkedIn withholds the body, prepare a JSON file from your complete original manuscript (not a scraped preview):

```json
{
  "source": "https://www.linkedin.com/pulse/YOUR-ARTICLE",
  "title": "Original article title",
  "author": "Richard Tang",
  "date": "2026-09-10T00:00:00Z",
  "complete": true,
  "paragraphs": ["First original paragraph.", "Second original paragraph."]
}
```

```sh
npm --prefix web/landing run blog:import -- 'https://www.linkedin.com/pulse/YOUR-ARTICLE' --slug your-article --input /absolute/path/original.json
```

The source URL must match. Plain-text export is intentionally narrow: no arbitrary HTML, scripts, or automatic remote asset fetching. Rich formatting and images require a reviewed follow-up edit. Crossposted copies on different platforms are not automatically merged; pick one canonical source to avoid duplicate pages.

## Review and release

```sh
npm --prefix web/landing test
npm --prefix web/landing run build
npm --prefix web/landing run dev
```

Review `/blog` and `/blog/your-article` locally, including original date, all paragraphs, links, captions, images, and mobile layout. The original-publication note preserves historical claims rather than recasting them as current product facts. JSON includes source URL and a retrieval SHA-256 receipt. Publishing remains the existing, separately authorized site-release workflow. This is an on-demand import pipeline, not automatic account monitoring.
