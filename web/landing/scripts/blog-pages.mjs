import { readFileSync } from 'node:fs';

const readPosts = () => JSON.parse(readFileSync(new URL('../src/content/posts.json', import.meta.url), 'utf8'));
const origin = 'https://proofpress.dev';
const repo = 'https://github.com/chenmingtang830/proofpress';
const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
const safeUrl = value => {
  try { const url = new URL(value, origin); return ['http:', 'https:'].includes(url.protocol) ? escape(url.href) : '#'; }
  catch { return '#'; }
};
const prettyDate = date => new Date(date).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' });

function inline(block, entities) {
  const styles = block.inlineStyleRanges ?? [];
  const ranges = block.entityRanges ?? [];
  const boundaries = [...new Set([0, block.text.length, ...[...styles, ...ranges].flatMap(r => [Math.min(r.offset, block.text.length), Math.min(r.offset + r.length, block.text.length)])])].sort((a,b) => a-b);
  return boundaries.slice(0,-1).map((start,i) => {
    let text = escape(block.text.slice(start, boundaries[i+1]));
    for (const style of styles.filter(r => r.offset <= start && start < r.offset+r.length)) {
      if (style.style === 'Bold') text = `<strong>${text}</strong>`;
      if (style.style === 'Italic') text = `<em>${text}</em>`;
      if (style.style === 'Code') text = `<code>${text}</code>`;
    }
    const range = ranges.find(r => r.offset <= start && start < r.offset+r.length);
    const entity = range && entities.get(String(range.key));
    if (entity?.type === 'LINK') text = `<a href="${safeUrl(entity.data.url)}">${text}</a>`;
    return text;
  }).join('');
}

function articleBody(post) {
  const entities = new Map(post.entities.map(e => [String(e.key),e.value]));
  let html = '', list = '';
  for (const block of post.blocks) {
    const desired = block.type === 'ordered-list-item' ? 'ol' : block.type === 'unordered-list-item' ? 'ul' : '';
    if (list !== desired) { if (list) html += `</${list}>`; if (desired) html += `<${desired}>`; list = desired; }
    if (block.type === 'atomic') {
      for (const range of block.entityRanges ?? []) {
        const entity = entities.get(String(range.key));
        for (const item of entity?.data?.mediaItems ?? []) {
          const media = post.media.find(m => m.id === item.mediaId);
          if (!media) throw new Error(`Missing article media in ${post.slug}`);
          const caption = entity?.data?.caption || `Illustration from the original article.`;
          html += `<figure><img src="${escape(media.src)}" width="${Number(media.width)}" height="${Number(media.height)}" loading="lazy" alt="${escape(caption)}"><figcaption>${escape(caption)} <a href="${safeUrl(post.source)}">View source</a></figcaption></figure>`;
        }
      }
      continue;
    }
    if (!block.text.trim()) continue;
    const tag = desired ? 'li' : block.type === 'header-two' ? 'h2' : block.type === 'header-three' ? 'h3' : block.type === 'blockquote' ? 'blockquote' : 'p';
    html += `<${tag}>${inline(block,entities)}</${tag}>`;
  }
  if (list) html += `</${list}>`;
  if (post.video) html += `<video controls playsinline preload="metadata" poster="${escape(post.image)}"><source src="${escape(post.video)}" type="video/mp4">Watch the <a href="${safeUrl(post.source)}">original demo</a>.</video>`;
  return html;
}

function card(post) {
  return `<a class="writingCard" href="/blog/${post.slug}"><div class="writingImage"><img src="${escape(post.image)}" alt="" width="1536" height="1024" loading="lazy"></div><span>${escape(post.label)} · ${prettyDate(post.date)}</span><h2>${escape(post.title)}</h2><p>${escape(post.description)}</p><small>Read article →</small></a>`;
}

function shell({ title, description, path, content, css, post, noindex = false }) {
  const posts = readPosts();
  const jsonLd = post ? { '@context': 'https://schema.org', '@type': 'BlogPosting', headline: post.title, description, datePublished: post.date, dateModified: post.modified, author: { '@type': 'Person', name: post.author, url: 'https://x.com/richardt830' }, publisher: { '@type': 'Organization', name: 'Proofpress', url: origin }, image: origin + post.image, mainEntityOfPage: origin + path, isBasedOn: post.source } : { '@context': 'https://schema.org', '@type': 'Blog', name: 'Proofpress Blog', url: origin+'/blog', blogPost: posts.map(p => ({ '@type': 'BlogPosting', headline: p.title, url: origin+'/blog/'+p.slug })) };
  return `<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)} | Proofpress</title><meta name="description" content="${escape(description)}">${noindex ? '<meta name="robots" content="noindex">' : ''}<link rel="canonical" href="${origin+path}"><link rel="icon" href="/logo.svg" type="image/svg+xml"><meta property="og:type" content="${post ? 'article' : 'website'}"><meta property="og:title" content="${escape(title)}"><meta property="og:description" content="${escape(description)}"><meta property="og:url" content="${origin+path}"><meta property="og:image" content="${origin+(post?.image ?? '/og-proofpress.png')}"><meta name="twitter:card" content="summary_large_image"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="${css}"><script type="application/ld+json">${JSON.stringify(jsonLd).replace(/</g,'\\u003c')}</script></head><body><div class="siteShell blogShell"><a class="skipLink" href="#main">Skip to content</a><header class="siteHeader"><a class="brand" href="/" aria-label="Proofpress home"><img src="/logo.svg" alt="" width="32" height="32"><span>Proofpress</span></a><nav aria-label="Primary navigation"><a href="/#product">Product</a><a href="/blog" aria-current="page">Blog</a><a href="${repo}#quick-start">Docs</a><a class="navContact" href="/#partners">Let’s talk →</a></nav><details class="mobileNav"><summary aria-label="Open navigation">Menu</summary><nav aria-label="Mobile navigation"><a href="/#product">Product</a><a href="/#teams">For teams</a><a href="/blog">Blog</a><a href="${repo}#quick-start">Docs</a></nav></details></header><main id="main">${content}</main><footer><a class="brand" href="/"><img src="/logo-on-dark.svg" alt="" width="28" height="28"><span>Proofpress</span></a><p>The Intelligence Ledger for agent-native research teams.</p><a href="${repo}">GitHub</a></footer></div></body></html>`;
}

export function renderBlog(path, css) {
  const posts = readPosts();
  if (path === '/blog') return shell({ title: 'Writing from the field', description: 'Research, product thinking, and field notes on governed knowledge for agents.', path, css, content: `<section class="blogIndex"><h1>Writing from the field.</h1><p class="narrativeLead">Research, product thinking, and notes on knowledge worth building on.</p><div class="blogGrid">${[...posts].sort((a,b)=>b.date.localeCompare(a.date)).map(card).join('')}</div></section>` });
  const post = posts.find(p => path === '/blog/'+p.slug);
  if (!post) return null;
  const note = post.slug === 'agents-create-a-new-knowledge-layer' ? 'This article preserves its original publication. Product availability has changed since then; see the current documentation for MCP, SDK, and Hosted setup.' : 'Preserved from the original publication. Product descriptions and research claims reflect that publication date.';
  return shell({ title: post.title, description: post.description, path, css, post, content: `<article class="blogArticle"><header class="articleHeader"><a href="/blog">← All writing</a><h1>${escape(post.title)}</h1><p class="articleByline">${escape(post.author)} · <time datetime="${escape(post.date)}">${prettyDate(post.date)}</time> · ${escape(post.label)}</p></header><img class="articleCover" src="${escape(post.image)}" alt="" width="1536" height="1024"><aside class="articleNote">${note} <a href="${safeUrl(post.source)}">Original publication</a> · <a href="${repo}#quick-start">Current documentation</a></aside><div class="articleBody">${articleBody(post)}</div><div class="articleEnd"><a href="/blog">← All writing</a><a href="/#product">Explore Proofpress →</a></div></article>` });
}

export function blogPages() {
  return {
    name: 'proofpress-static-blog',
    configureServer(server) {
      server.middlewares.use((req,res,next) => {
        const path = new URL(req.url ?? '/', 'http://localhost').pathname.replace(/\/$/,'');
        if (path !== '/blog' && !path.startsWith('/blog/')) return next();
        const html = renderBlog(path, '/src/index.css');
        res.statusCode = html ? 200 : 404;
        res.setHeader('Content-Type','text/html; charset=utf-8');
        res.end(html ?? shell({title:'Article not found',description:'This article is not available.',path,css:'/src/index.css',noindex:true,content:'<section class="blogIndex"><h1>Article not found.</h1><a href="/blog">Browse all writing →</a></section>'}));
      });
    },
    generateBundle(_options,bundle) {
      const posts = readPosts();
      const css = Object.values(bundle).find(file => file.type === 'asset' && file.fileName.endsWith('.css'));
      if (!css) throw new Error('Missing stylesheet for static blog');
      const paths = ['/blog', ...posts.map(p => '/blog/'+p.slug)];
      for (const path of paths) this.emitFile({type:'asset',fileName:path.slice(1)+'.html',source:renderBlog(path,'/'+css.fileName)});
      this.emitFile({type:'asset',fileName:'sitemap.xml',source:`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${['/',...paths].map(path=>`<url><loc>${origin+path}</loc></url>`).join('')}</urlset>`});
      this.emitFile({type:'asset',fileName:'robots.txt',source:`User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`});
    },
  };
}
