import { useEffect, useRef, useState } from "react";
import { ArrowRight01Icon } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { Button, ButtonLink } from "./components/button";
import { ModelResultsChart } from "./components/model-results-chart";
import { KnowledgeThread } from "./components/knowledge-thread";
import { LivingResearch } from "./components/living-research";
import { KnowledgeConfluence } from "./components/knowledge-confluence";
import { useScenePaging } from "./components/use-scene-paging";
import posts from "./content/post-index.json";
import "./customer-home.css";
import "./living-home.css";

const repoUrl = "https://github.com/chenmingtang830/proofpress";
const contactUrl = "https://ancient-ball-940.notion.site/eacf21eef9b54c3287f72892cd024a1c?pvs=105";
// Local review export; publish to media storage with the approved website release.
const brandFilmUrl = "/films/proofpress-continuara-20261021-1080p.mp4";
const studyUrl = `${repoUrl}/blob/main/studies/long-horizon-eval/relaybench/PUBLIC_RESULTS.md`;
const tokenStudyUrl = `${repoUrl}/blob/main/studies/apex-agent-eval/ara/evidence/tables/table3_cross_task_summary.md`;
const featuredSlug = "atom-bit-commit-agent-knowledge";
const writing = [...posts].sort((a, b) => {
  if (a.slug === featuredSlug) return -1;
  if (b.slug === featuredSlug) return 1;
  return Date.parse(b.date) - Date.parse(a.date);
});
const formatArticleDate = (date: string) => new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }).format(new Date(date));
function Arrow() { return <HugeiconsIcon icon={ArrowRight01Icon} size={18} strokeWidth={1.6} aria-hidden="true" />; }
function closeMobileNav(event: React.MouseEvent<HTMLAnchorElement>) { event.currentTarget.closest("details")?.removeAttribute("open"); }

export function App() {
  useScenePaging();
  const journeyRef = useRef<HTMLDivElement>(null);
  const writingRail = useRef<HTMLDivElement>(null);
  const [railEdges, setRailEdges] = useState({ start: true, end: false });
  const syncRail = () => {
    const rail = writingRail.current;
    if (rail) setRailEdges({ start: rail.scrollLeft < 2, end: rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 2 });
  };
  useEffect(() => {
    const rail = writingRail.current;
    if (!rail) return;
    const observer = new ResizeObserver(syncRail); observer.observe(rail); syncRail();
    return () => observer.disconnect();
  }, []);
  const moveWriting = (direction: number) => {
    const rail = writingRail.current;
    const card = rail?.firstElementChild as HTMLElement | null;
    if (rail && card) rail.scrollBy({ left: direction * (card.offsetWidth + 24), behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
  };
  return <div className="siteShell customerHome threadHome">
    <a className="skipLink" href="#main">Skip to content</a>
      <header className="siteHeader">
        <a className="brand" href="#top" aria-label="Proofpress home">
          <img src="/logo.svg" alt="" width="32" height="32" />
          <span>Proofpress</span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="#product">Product</a>
          <a href="#teams">Use cases</a>
          <a href="#evidence">Evidence</a>
          <a href="/blog">Blog</a>
          <a href={`${repoUrl}#quick-start`}>Docs</a>
          <a className="navContact" href={contactUrl}>Let’s talk <Arrow /></a>
        </nav>
        <details className="mobileNav">
          <summary aria-label="Open navigation">Menu</summary>
          <nav aria-label="Mobile navigation">
            <a href="#product" onClick={closeMobileNav}>Product</a>
            <a href="#teams" onClick={closeMobileNav}>Use cases</a>
            <a href="#evidence" onClick={closeMobileNav}>Evidence</a>
            <a href="/blog" onClick={closeMobileNav}>Blog</a>
            <a href={`${repoUrl}#quick-start`} onClick={closeMobileNav}>Docs</a>
          </nav>
        </details>
      </header>

      <main id="main">
        <div className="knowledgeJourney" ref={journeyRef}>
          <KnowledgeThread journeyRef={journeyRef} revised={false} />
          <section className="journeySection journeyHero" id="top" aria-labelledby="hero-title">
            <div className="journeyCopy">
              <h1 id="hero-title">Build on every discovery.</h1>
              <p className="journeyLead">The typed knowledge system for RSI.</p>
              <div className="heroActions"><ButtonLink href={repoUrl}>GitHub <Arrow /></ButtonLink><a className="journeyTextLink" href={contactUrl}>Let’s talk</a></div>
            </div>
            <div className="threadScene heroThreadScene" data-thread-scene="beginning" aria-hidden="true" />
          </section>

          <section className="journeySection journeyScattered" aria-labelledby="scattered-title">
            <div className="journeyCopy">
              <h2 id="scattered-title">The result is saved.<br />The reasoning is scattered.</h2>
              <div className="researchFragments" aria-label="Illustrative research materials scattered across files and conversations">
                <div className="researchFragment markdownDraft"><span className="fileName">experiment-notes.md</span><pre><span className="mdSyntax">##</span> A promising result{"\n"}<span className="mdSyntax">- [x]</span> Try the revised protocol{"\n"}<span className="mdSyntax">- [ ]</span> Check another sample set{"\n\n"}<span className="mdSyntax">&gt;</span> Better recovery. Why?</pre><span className="paperNote">need the conditions</span></div>
                <div className="researchFragment conversationNote"><span>Team conversation</span><p>"Did we already try this?"</p><small>The answer is somewhere in the notes.</small></div>
                <div className="researchFragment failedAttempt"><span className="fileName">earlier-attempt.md</span><pre><span className="mdSyntax">#</span> What didn’t work{"\n"}<del>Repeat the original setup</del>{"\n\n"}Different samples.{"\n"}Same conclusion?</pre><span className="marginQuery">see last month’s run</span></div>
                <div className="researchFragment looseReference"><span className="fileName">results / final-v3.csv</span><div className="sampleRows" aria-hidden="true"><span>sample</span><span>method</span><span>notes</span><span>A / B</span><span>revised</span><span>?</span><span>C / D</span><span>original</span><span>check</span></div></div>
                <div className="researchFragment smallScrap"><span className="fileName">handoff.md</span><p>"Ask Maya.<br />She remembers the exception."</p></div>
              </div>
              <p className="scatteredAfterword">Your team has to piece it back together. Every time.</p>
            </div>
            <div className="threadScene" data-thread-scene="scattered" />
          </section>

          <section className="journeySection journeyProduct" id="product" aria-labelledby="product-title">
            <LivingResearch />
            <div className="productThreadAnchor" data-thread-scene="connected" />

          </section>

          <section className="journeySection journeyForward" id="teams" aria-labelledby="teams-title">
            <div className="journeyCopy">
              <h2 id="teams-title">Pick up where the last experiment left off.</h2>
              <table className="reuseComparison" aria-label="Research without and with Proofpress">
                <thead><tr><th scope="col">The old way</th><th scope="col">With Proofpress</th></tr></thead>
                <tbody>
                  {[
                    ["Repeat the same failed attempts.", "Keep what failure taught you."],
                    ["Rebuild the evidence. Again.", "Reuse findings with their evidence."],
                    ["Start each run from scratch.", "Build on the last experiment."],
                  ].map(([before, after]) => <tr key={before}>
                    <td><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6L18 18M18 6L6 18" /></svg><span>{before}</span></td>
                    <td><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12L9 17L20 6" /></svg><span>{after}</span></td>
                  </tr>)}
                </tbody>
              </table>
            </div>
            <div className="threadScene" data-thread-scene="forward" />
          </section>

          <section className="journeySection journeyResearch" id="evidence" aria-labelledby="evidence-title">
            <div className="journeyCopy"><h2 id="evidence-title">Higher performance. Fewer tokens.<br />Fewer errors.</h2></div>
            <div className="evidenceOverview">
              <div className="evidenceChart"><div className="studyHeadline"><strong>89.3% <span>→</span> 93.4%</strong><p>Rubric completion across seven models</p></div><ModelResultsChart /><p className="studyScope">Proofpress-run study · 126 paired runs · Harvey LAB-derived tasks.</p><a href={studyUrl}>Results &amp; methodology <Arrow /></a></div>
              <div className="evidenceSide">
                <div><strong>5.5×</strong><h3>Fewer numeric errors</h3><p>11 → 2 incorrect values</p><small>20 paired chains<br />1,600 numeric slots per arm</small></div>
                <div><strong>38.3%</strong><h3>Fewer executor tokens</h3><p>Muse Spark 1.1</p><small>A separate two-task APEX pilot.<br />Executor tokens only; excludes upstream preparation.</small><a href={tokenStudyUrl}>Pilot results <Arrow /></a></div>
              </div>
            </div>
            <p className="evidencePublication">Capture, Verify, Govern · Accepted, IEEE NANDA Workshop</p>
            <div className="threadScene quietThreadScene" data-thread-scene="research" />
          </section>

          <section className="journeySection journeyMission" id="mission" aria-labelledby="film-title">
            <KnowledgeConfluence />
            <div className="missionClosing">
              <div className="missionOpening">
                <div className="journeyCopy"><h2 id="film-title">Knowledge worth<br />building on.</h2><p>Every discovery carries something forward.<br />Build a body of knowledge the next person can build on.</p><p className="missionSignature">Our mission</p></div>
              </div>
              <video controls playsInline preload="metadata" poster="/proofpress-shoulders-poster-20260910.webp"><source src={brandFilmUrl} type="video/mp4" />Your browser does not support embedded video.</video>
            </div>
          </section>
        </div>
        <section className="writing" id="writing" aria-labelledby="writing-title">
          <div className="compactIntro">
            <h2 id="writing-title">Writing from the field.</h2>
            <a href="/blog">Read the blog <Arrow /></a>
          </div>
          <div className="writingNavigation" aria-label="Browse articles">
            <Button variant="secondary" aria-label="Previous articles" aria-controls="writing-rail" disabled={railEdges.start} onClick={() => moveWriting(-1)}><span className="previousArrow"><Arrow /></span></Button>
            <Button variant="secondary" aria-label="Next articles" aria-controls="writing-rail" disabled={railEdges.end} onClick={() => moveWriting(1)}><Arrow /></Button>
          </div>
          <div className="writingGrid" id="writing-rail" ref={writingRail} onScroll={syncRail} tabIndex={0} role="region" aria-label="Articles, featured first; scroll horizontally">
            {writing.map((item) => (
              <a className="writingCard" href={`/blog/${item.slug}`} key={item.slug}>
                <div className="writingImage">
                  <img
                    src={item.image}
                    alt=""
                    width={1600}
                    height={900}
                    loading="lazy"
                    decoding="async"
                  />
                </div>
                <span>{item.label} · {formatArticleDate(item.date)}</span>
                <h3>{item.title}</h3>
                <small>Read article <Arrow /></small>
              </a>
            ))}
          </div>
        </section>

        <section className="finalCta" id="partners" aria-labelledby="cta-title">
          <div><h2 id="cta-title">For those who move knowledge forward.</h2></div>
          <div className="finalCtaAction"><p>Tell us what your team is working on.</p><ButtonLink href={contactUrl}>Let’s talk <Arrow /></ButtonLink></div>
        </section>
      </main>
      <footer>
        <a className="brand" href="#top" aria-label="Back to top">
          <img src="/logo-on-dark.svg" alt="" width="28" height="28" />
          <span>Proofpress</span>
        </a>
        <div className="footerIdentity">
          <small>by <span>Continuara Labs</span></small>
        </div>
        <a href={repoUrl}>GitHub</a>
      </footer>
  </div>;
}
