import test from 'node:test';
import assert from 'node:assert/strict';
import {sourceUrl,upsert,normalizeExport,linkedinArticle} from './import-blog.mjs';
import {renderBlog} from './blog-pages.mjs';

test('source URLs reject unrelated authors, credentials, schemes, and hosts',()=>{
  for (const url of ['http://x.com/richardt830/status/123','https://x.com/other/status/123','https://x.com.evil.test/richardt830/status/123','https://user@x.com/richardt830/status/123','https://localhost/pulse/a','https://www.linkedin.com/login']) assert.throws(()=>sourceUrl(url));
  assert.equal(sourceUrl('https://twitter.com/richardt830/status/123?s=20').url,'https://x.com/richardt830/status/123');
});
test('duplicates are no-ops; updates retain stable URLs and unrelated posts',()=>{
  const post={source:'https://x.com/richardt830/status/123',slug:'one'};
  const posts=[post];
  assert.equal(upsert(posts,{...post,title:'changed'}),posts);
  assert.equal(upsert(posts,{...post,title:'changed'},true)[0].title,'changed');
  assert.throws(()=>upsert(posts,{...post,slug:'two'},true));
  assert.throws(()=>upsert(posts,{...post,source:'https://x.com/richardt830/status/124'}));
});
const original={title:'Synthetic test article',author:'Richard Tang',date:'2026-09-10',complete:true,paragraphs:['Original content.']};
test('fallback requires explicit complete original content and original date/author',()=>{
  assert.equal(normalizeExport(original).blocks[0].text,'Original content.');
  for(const bad of [{complete:false},{author:'Someone else'},{date:'yesterday'},{paragraphs:[]}]) assert.throws(()=>normalizeExport({...original,...bad}));
});
test('LinkedIn structured full text only; login walls and excerpts fail closed',()=>{
  const data={'@type':'Article',headline:original.title,author:{name:'Richard Tang'},datePublished:original.date,articleBody:'Synthetic fixture paragraph. '.repeat(30)};
  const html=`<script type="application/ld+json">${JSON.stringify(data)}</script>`;
  assert.equal(linkedinArticle(html).title,original.title);
  assert.throws(()=>linkedinArticle('<h1>Sign in</h1>'));
  assert.throws(()=>linkedinArticle(html.replace(data.articleBody,'Excerpt')));
});
test('blog emits native full article, metadata, captions, and missing route null',()=>{
  const html=renderBlog('/blog/memory-is-not-enough','/style.css');
  assert.ok(html.includes('Memory Is Not Enough'));
  assert.ok(html.includes('application/ld+json'));
  assert.ok(html.includes('Shared memory can amplify a weak claim'));
  assert.ok(html.includes('<blockquote>'));
  assert.ok(!html.includes('src="https://proofpress.dev/blog-media/'));
  assert.equal(renderBlog('/blog/not-an-article','/style.css'),null);
});
