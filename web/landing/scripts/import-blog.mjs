// Explicit local import only. Never called by builds or publication hooks.
import { mkdir, readFile, writeFile, rename } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

const destination = new URL('../src/content/posts.json', import.meta.url);
const mediaDir = new URL('../public/blog-media/', import.meta.url);
const hash = value => createHash('sha256').update(value).digest('hex');
const block = text => ({type:'unstyled',text,entityRanges:[],inlineStyleRanges:[]});

async function writeIndex(posts) {
  const index=posts.map(({slug,title,date,label,image})=>({slug,title,date,label,image}));
  const target=new URL('post-index.json',destination);
  const content=JSON.stringify(index,null,2)+'\n';
  try { if (await readFile(target,'utf8') === content) return; } catch (error) { if(error.code !== 'ENOENT') throw error; }
  const temp=new URL('post-index.json.tmp',destination);
  await writeFile(temp,content); await rename(temp,target);
}

export function sourceUrl(input) {
  const url = new URL(input);
  if (url.protocol !== 'https:' || url.username || url.password || url.port) throw new Error('Expected a public HTTPS article URL');
  if (['x.com','www.x.com','twitter.com','www.twitter.com'].includes(url.hostname)) {
    const match = url.pathname.match(/^\/richardt830\/status\/(\d+)\/?$/i);
    if (!match) throw new Error('X imports are restricted to richardt830 status URLs');
    return {platform:'X',id:match[1],url:`https://x.com/richardt830/status/${match[1]}`};
  }
  if (['linkedin.com','www.linkedin.com'].includes(url.hostname) && /^\/(pulse|posts)\/[^/]+\/?$/.test(url.pathname)) return {platform:'LinkedIn',url:`https://www.linkedin.com${url.pathname.replace(/\/$/,'')}`};
  throw new Error('Only X status and LinkedIn pulse/posts URLs are supported');
}

export function upsert(posts, post, replace = false) {
  const existing = posts.find(p => sourceUrl(p.source).url === post.source);
  if (existing && !replace) return posts;
  if (existing && existing.slug !== post.slug) throw new Error('Preserve the existing slug when replacing an article');
  if (posts.some(p => p.slug === post.slug && p !== existing)) throw new Error('Slug already belongs to another article');
  return existing ? posts.map(p => p === existing ? post : p) : [...posts,post];
}

export function normalizeExport(data) {
  if (!data.title?.trim() || !data.author?.trim() || !data.date || !Number.isFinite(Date.parse(data.date))) throw new Error('Export requires title, author, and an ISO publication date');
  if (data.author !== 'Richard Tang') throw new Error('Only Richard Tang authored exports are allowed');
  if (data.complete !== true) throw new Error('Confirm complete original content with complete: true; excerpts are not importable');
  if (!Array.isArray(data.paragraphs) || !data.paragraphs.length || data.paragraphs.some(p => typeof p !== 'string' || !p.trim())) throw new Error('Export requires original paragraphs as nonempty strings');
  return {title:data.title,author:data.author,date:new Date(data.date).toISOString(),modified:new Date(data.modified ?? data.date).toISOString(),blocks:data.paragraphs.map(block),entities:[],media:[]};
}

export function linkedinArticle(html) {
  const objects = [...html.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)].flatMap(match => {
    try { const value = JSON.parse(match[1]); return Array.isArray(value) ? value : value['@graph'] ?? [value]; } catch { return []; }
  });
  const article = objects.find(o => ['Article','BlogPosting','NewsArticle'].includes(o['@type']) && typeof o.articleBody === 'string');
  if (!article || article.isAccessibleForFree === false || article.articleBody.length < 500 || /(?:sign in to (?:read|continue)|see more|read more)\s*[.…]*$/i.test(article.articleBody)) throw new Error('LinkedIn did not expose a complete public article. Use --input with your complete original export; no excerpt was saved.');
  const author = Array.isArray(article.author) ? article.author[0] : article.author;
  return normalizeExport({title:article.headline,author:author?.name,date:article.datePublished,modified:article.dateModified,paragraphs:article.articleBody.split(/\n\s*\n/).filter(p=>p.trim()),complete:true});
}

async function request(url, kind = 'source') {
  const parsed = new URL(url);
  const allowed = kind === 'media' ? ['pbs.twimg.com','video.twimg.com'] : ['api.fxtwitter.com','www.linkedin.com'];
  if (parsed.protocol !== 'https:' || !allowed.includes(parsed.hostname) || parsed.port || parsed.username || parsed.password) throw new Error('Unexpected download host');
  const response = await fetch(parsed,{redirect:'error',signal:AbortSignal.timeout(30000)});
  if (!response.ok) throw new Error(`Import unavailable (HTTP ${response.status}); retry later or use an original export`);
  return response;
}

async function download(url, filename) {
  const response = await request(url,'media');
  const bytes = Buffer.from(await response.arrayBuffer());
  if (bytes.length > 40 * 1024 * 1024) throw new Error('Media exceeds the 40 MB import limit');
  await mkdir(mediaDir,{recursive:true});
  await writeFile(new URL(filename,mediaDir),bytes);
  return `/blog-media/${filename}`;
}

export async function main(args) {
  const [input,...flags] = args;
  if (!input) throw new Error('Usage: npm run blog:import -- URL --slug stable-slug [--input original.json] [--title title] [--replace]');
  const options = {};
  for (let i=0;i<flags.length;i++) {
    const name=flags[i];
    if (name === '--replace') options.replace=true;
    else if (['--slug','--input','--title'].includes(name) && flags[i+1] && !flags[i+1].startsWith('--')) options[name.slice(2)] = flags[++i];
    else throw new Error(`Unknown or incomplete option: ${name}`);
  }
  const source = sourceUrl(input);
  const posts = JSON.parse(await readFile(destination,'utf8'));
  const existing = posts.find(p=>sourceUrl(p.source).url === source.url);
  if (existing && !options.replace) { await writeIndex(posts); console.log(`Already imported: /blog/${existing.slug} (unchanged)`); return; }
  const slug = options.slug ?? existing?.slug;
  if (!slug || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) throw new Error('Provide --slug with lowercase words separated by hyphens');
  if (posts.some(p=>p.slug === slug && p !== existing)) throw new Error('Slug already belongs to another article');
  let post, raw, retrievedFrom, image='/og-proofpress.png';
  if (options.input) {
    raw=await readFile(options.input,'utf8');
    const data=JSON.parse(raw);
    if (sourceUrl(data.source).url !== source.url) throw new Error('Export source does not match requested URL');
    post=normalizeExport(data); retrievedFrom='user-provided original export';
  } else if (source.platform === 'LinkedIn') {
    raw=await (await request(source.url)).text();
    post=linkedinArticle(raw); retrievedFrom=source.url;
  } else {
    retrievedFrom=`https://api.fxtwitter.com/status/${source.id}`;
    raw=await (await request(retrievedFrom)).text();
    const tweet=JSON.parse(raw).tweet;
    if (tweet?.author?.screen_name !== 'richardt830' || String(tweet.id) !== source.id) throw new Error('Unexpected X author or post');
    const article=tweet.article;
    if (!article && !options.title) throw new Error('A regular post requires --title; no title is invented');
    const blocks=article?.content?.blocks ?? tweet.text.split('\n\n').map(block);
    if (!blocks?.length) throw new Error('Source has no article body');
    const media=[];
    for (const item of article?.media_entities ?? []) {
      const info=item.media_info;
      if (!/^\d+$/.test(String(item.media_id))) throw new Error('Invalid media identifier');
      const src=await download(info.original_img_url,`${item.media_id}.jpg`);
      media.push({id:item.media_id,src,width:info.original_img_width,height:info.original_img_height,source:info.original_img_url});
    }
    const cover=article?.cover_media?.media_info;
    if (cover?.original_img_url) image=await download(cover.original_img_url,`${source.id}-cover.jpg`);
    else if (media[0]) image=media[0].src;
    const videoUrl=tweet.media?.videos?.[0]?.formats?.find(f=>f.bitrate === 2176000)?.url;
    const video=videoUrl ? await download(videoUrl,`${source.id}.mp4`) : undefined;
    const date=article?.created_at ?? new Date(tweet.created_timestamp*1000).toISOString();
    post={title:article?.title ?? options.title,author:'Richard Tang',date,modified:article?.modified_at ?? date,blocks,entities:article?.content.entityMap ?? [],media,video};
  }
  post={...post,slug,label:'ARTICLE',image,source:source.url,platform:source.platform,description:post.blocks.find(b=>b.type === 'unstyled' && b.text.trim())?.text.slice(0,240) ?? post.title,importReceipt:{retrievedFrom,retrievedAt:new Date().toISOString(),sha256:hash(raw)}};
  const result=upsert(posts,post,options.replace);
  const temp=new URL('posts.json.tmp',destination);
  await writeFile(temp,JSON.stringify(result,null,2)+'\n');
  await rename(temp,destination);
  await writeIndex(result);
  console.log(`Imported locally: /blog/${slug} (${post.blocks.length} blocks, ${post.media.length} body images). Review before publishing.`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main(process.argv.slice(2)).catch(error=>{console.error(error.message);process.exitCode=1;});
