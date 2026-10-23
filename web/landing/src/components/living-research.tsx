import { useEffect, useLayoutEffect, useRef, useState } from "react";
import "./living-research.css";

const steps = [
  { label: "Capture", message: "Keep the finding.\nKeep its basis.", description: "Results, evidence, and conditions stay connected." },
  { label: "Verify", message: "Deterministic checks.\nLM-as-judge.\nHuman approval.", description: "Deterministic checks and LM-as-judge inform review. Human Approval authorizes reuse." },
  { label: "Reuse", message: "Give the next run\na head start.", description: "Reuse a reviewed finding within its declared scope." },
  { label: "Learn", message: "Every run teaches\nthe next.", description: "Product direction preview: outcomes attributed to a claim and its context update selection weight for similar tasks. Evidence confidence and approval remain separate." },
  { label: "Review", message: "New evidence.\nKnow what needs review.", description: "Review the finding and its recorded downstream uses." },
];

// Learn has two consecutive scroll states under the same navigation item.
const scrollPhases = [0, 1, 2, 3, 3, 4] as const;

/** Scroll chooses the state; it never consumes, delays, or redirects wheel input. */
export function LivingResearch() {
  const root = useRef<HTMLDivElement>(null);
  const stage = useRef<HTMLDivElement>(null);
  const returnRoute = useRef<SVGPathElement>(null);
  const feedbackRoute = useRef<SVGPathElement>(null);
  const [feedbackArrived, setFeedbackArrived] = useState(false);
  const exitRoute = useRef<SVGPathElement>(null);
  const focalMarker = useRef<SVGGElement>(null);
  const bounds = useRef({ top: 0, travel: 1 });
  const [scrollIndex, setScrollIndex] = useState(0);
  const phase = scrollPhases[scrollIndex];
  const outcome = scrollIndex === 4 ? "failure" : "success";
  const [compact, setCompact] = useState(false);
  const [manual, setManual] = useState(false);
  const [inView, setInView] = useState(false);
  const [entryX, setEntryX] = useState(-40);
  const [entryY, setEntryY] = useState(-240);
  const [exitY, setExitY] = useState(440);
  const [exiting, setExiting] = useState(false);
  const [bridge, setBridge] = useState({ x: -48, width: 1000, height: 110 });
  useEffect(() => {
    const svg = stage.current?.querySelector<SVGSVGElement>(".researchStateDiagram svg");
    if (!svg) return;
    const measureEntry = () => {
      const matrix = svg.getScreenCTM(), panel = stage.current?.getBoundingClientRect();
      if (!matrix || !panel) return;
      const entry = new DOMPoint(25, panel.top).matrixTransform(matrix.inverse());
      setEntryX(entry.x); setEntryY(entry.y);
      setExitY(new DOMPoint(0, panel.bottom).matrixTransform(matrix.inverse()).y);
      const section = stage.current?.closest<HTMLElement>("section");
      const story = root.current;
      if (section && story) {
        const next = { x: 25 - story.getBoundingClientRect().left, width: story.clientWidth, height: Math.max(0, section.clientHeight - story.offsetTop - story.offsetHeight) };
        setBridge(current => current.x === next.x && current.width === next.width && current.height === next.height ? current : next);
      }
    };
    let frame = 0, disposed = false;
    const schedule = () => { if (disposed) return; cancelAnimationFrame(frame); frame = requestAnimationFrame(measureEntry); };
    const observer = new ResizeObserver(schedule); observer.observe(svg.parentElement!); if (root.current?.closest("section")) observer.observe(root.current.closest("section")!); schedule();
    document.fonts.ready.then(schedule);
    window.addEventListener("resize", schedule);
    return () => { disposed = true; observer.disconnect(); cancelAnimationFrame(frame); window.removeEventListener("resize", schedule); };
  }, [compact]);
  useEffect(() => {
    if (!stage.current) return;
    const observer = new IntersectionObserver(([entry]) => setInView(entry.isIntersecting), { threshold: .2 });
    observer.observe(stage.current);
    return () => observer.disconnect();
  }, []);
  useLayoutEffect(() => {
    const route = exiting ? exitRoute.current : phase === 2 ? returnRoute.current : phase === 3 ? feedbackRoute.current : null, marker = focalMarker.current;
    setFeedbackArrived(false);
    if (!inView || !route || !marker) return;
    if (phase === 3 && !exiting && returnRoute.current) {
      const parked = returnRoute.current.getPointAtLength(returnRoute.current.getTotalLength());
      marker.style.transform = `translate(${parked.x}px, ${parked.y}px)`;
    }
    const length = route.getTotalLength();
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let frame = 0;
    const started = performance.now();
    const move = (time: number) => {
      const progress = reduced ? 1 : Math.min(1, (time - started) / 1100);
      const point = route.getPointAtLength(length * (1 - (1 - progress) ** 3));
      if (phase === 3 && !exiting) {
        // Feedback is a signal, not the finding travelling back from the next run.
        route.style.strokeDashoffset = `${(1 - progress) * 48}`;
      } else marker.style.transform = `translate(${point.x}px, ${point.y}px)`;
      if (progress < 1) frame = requestAnimationFrame(move);
      else if (phase === 3 && !exiting) setFeedbackArrived(true);
    };
    move(started);
    return () => cancelAnimationFrame(frame);
  }, [phase, inView, compact, exiting, entryX, exitY, outcome]);
  useEffect(() => {
    const element = root.current, panel = stage.current;
    if (!element || !panel) return;
    let frame = 0, disposed = false;
    const update = () => {
      frame = 0;
      if (bounds.current.travel <= 1) return;
      const progress = (window.scrollY - bounds.current.top) / bounds.current.travel;
      setScrollIndex(Math.max(0, Math.min(scrollPhases.length - 1, Math.floor(progress * scrollPhases.length))));
      setExiting(progress > .93);
    };
    const measure = () => {
      if (disposed) return;
      const inset = window.innerWidth <= 760 ? 64 : 72;
      bounds.current = { top: element.getBoundingClientRect().top + window.scrollY - inset, travel: Math.max(1, element.offsetHeight - panel.offsetHeight) };
      setCompact(window.innerWidth <= 1000);
      setManual(bounds.current.travel <= 1);
      update();
    };
    const onScroll = () => { if (!frame) frame = requestAnimationFrame(update); };
    const observer = new ResizeObserver(measure);
    observer.observe(element); observer.observe(panel);
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", measure);
    document.fonts.ready.then(measure);
    measure();
    return () => { disposed = true; observer.disconnect(); cancelAnimationFrame(frame); window.removeEventListener("scroll", onScroll); window.removeEventListener("resize", measure); };
  }, []);
  const selectStep = (index: number) => {
    const targetIndex = index === 4 ? 5 : index;
    if (bounds.current.travel <= 1) { setScrollIndex(targetIndex); setExiting(false); return; }
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scrollTo({ top: bounds.current.top + bounds.current.travel * (targetIndex === 0 ? 0 : (targetIndex + .15) / scrollPhases.length), behavior: reduced ? "instant" : "smooth" });
  };
  const step = steps[phase];
  const focalPoint = !inView ? [entryX, compact ? 170 : 84] : (compact ? [[390,170],[440,180],[380,310],[380,310],[390,170]] : [[126,88.17],[300,170],[214,237],[214,237],[390,170]])[phase];
  const point = inView && exiting ? [entryX, exitY] : focalPoint;
  const entryTurn = compact ? 130 : 16;
  const entrySpan = entryTurn - entryY;
  return <div className="researchStory" ref={root}>
    <div className="researchStoryStage" ref={stage} data-scroll-state={scrollIndex} data-phase={phase} data-in-view={inView} data-exiting={exiting}>
      <div className="productStoryHeading"><h2 id="product-title">A typed knowledge system.</h2><p>Every finding carries its <strong>evidence, scope, and validity.</strong></p></div>
      <nav className="researchSteps" aria-label="Explore the knowledge lifecycle">
        {steps.map((item, index) => <button type="button" key={item.label} aria-current={phase === index ? "step" : undefined} onClick={() => selectStep(index)}><span className="stepIndicator" />{item.label}</button>)}
      </nav>
      <div className="statefulResearch" data-state={step.label.toLowerCase()} data-outcome={outcome} data-feedback-arrived={feedbackArrived}>
        <div className="researchStateDiagram">
          <svg viewBox={compact ? "340 0 400 340" : "0 0 740 340"} role="img" aria-label={`${step.label}: an experiment, a verification gate, and connected findings`}>
            <defs><marker id="lifecycle-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M1 1 L8 5 L1 9" fill="none" stroke="currentColor" strokeWidth="1.5" /></marker></defs>
            <path className="stateEntry" d={`M${entryX} ${entryY} C${entryX} ${entryY + entrySpan * .32} ${entryX - 18} ${entryY + entrySpan * .72} ${entryX + 10} ${entryTurn} ${compact ? `C${entryX + 22} 168 350 170 390 170` : `C${entryX + 28} 54 74 42 126 88.17`}`} />
            <g className="stateResearchCycle"><path d="M43 139 A94 94 0 0 1 210 139 M210 220 A94 94 0 0 1 43 220" markerEnd="url(#lifecycle-arrow)" /><text x="126" y="175" textAnchor="middle">Research</text><text x="126" y="202" textAnchor="middle">cycle</text><text className="cycleSmall" x="126" y="38" textAnchor="middle">Experiment · evaluate · learn</text></g>
            <path className="stateTransfer" d="M220 144 C257 144 261 170 300 170 L367 170" markerEnd="url(#lifecycle-arrow)" />
            <g className="stateGate"><path d="M300 126 V235" /><text x="300" y="83" textAnchor="middle">Verification gate</text><text x="300" y="105" textAnchor="middle">Policy + human review</text></g>
            <path ref={returnRoute} className="stateReturn" d={compact ? "M490 230 C490 300 460 320 380 310" : "M490 234 C490 335 292 350 214 237"} markerEnd="url(#lifecycle-arrow)" /><text className="returnLabel" x="333" y="330" textAnchor="middle">{phase === 3 ? "Reuse outcome" : "Reuse within scope"}</text>
            {compact && (phase === 2 || phase === 3) && <g className="compactReuseTarget"><circle cx="380" cy="310" r="12" /><text x="403" y="316">Next run</text></g>}
            <path ref={feedbackRoute} className="stateFeedback" d={compact ? "M380 310 C460 320 490 300 490 230" : "M214 237 C292 350 490 335 490 234"} markerEnd="url(#lifecycle-arrow)" />
            <g className="stateKnowledge"><path className="stateRelation" d="M390 170 L490 190 L553 98 L656 162 L592 265 L490 190 M390 170 L403 270 L592 265 M553 98 L656 162" />
              <path className="contextWeight" d="M490 190 L553 98 L656 162 M490 190 L592 265" />
              <circle className="stateEvidence" cx="390" cy="170" r="13" /><circle className="stateEvidence" cx="403" cy="270" r="10" />
              <circle className="stateNode weightedNode upperWeightedNode" cx="553" cy="98" r="22" /><circle className="stateNode weightedNode farWeightedNode" cx="656" cy="162" r="28" /><circle className="stateNode weightedNode lowerWeightedNode" cx="592" cy="265" r="22" />
              <g className="weightAnnotation"><text x="520" y="35" textAnchor="middle">{feedbackArrived ? (outcome === "success" ? "Stronger fit" : "Lower weight · Review") : "Outcome feedback"}</text><text x="520" y="57" textAnchor="middle">For similar tasks</text></g>
              <circle className="stateFocusRing" cx="490" cy="190" r="44" /><circle className="stateFocus" cx="490" cy="190" r="35" /><text className="stateInitial" x="490" y="198" textAnchor="middle">A</text>
              <text className="evidenceLabel" x="392" y="142" textAnchor="middle">{phase === 4 ? "Evidence changed" : "Evidence"}</text>
              <path className="reviewSignal" d="M403 172 L454 183" markerEnd="url(#lifecycle-arrow)" />
              {phase === 4 && <text className="reviewLabel" x="490" y="250" textAnchor="middle">Needs review</text>}
            </g>
            <path ref={exitRoute} className="stateExit" d={`M490 225 C480 310 368 345 240 350 C105 355 ${entryX} ${exitY - 130} ${entryX} ${exitY}`} />
            <g ref={focalMarker} className="researchFocalPoint" data-reusing={phase === 2 || phase === 3 || exiting} style={{ transform: `translate(${point[0]}px, ${point[1]}px)` }} aria-hidden="true">
              <circle className="focalSurface" r="10" />
              <circle className="focalDot" r="6" />
            </g>
          </svg>
        </div>
        <div className="stateMessage" role="region" aria-label={`${step.label}: ${step.description}`}>
          <h3>{step.message}</h3>
          {phase === 3 && <div className="outcomeLearning">
            <p className="outcomeStatus" aria-live="polite">{outcome === "success" ? "Successful run" : "Failed run"}</p>
            <p>Utility learns. Approval stays separate.</p>
          </div>}
        </div>
      </div>
      <div className="researchStoryFoot"><span>{phase === 3 ? "Outcome-learning preview" : "Illustrative finding history"} · {scrollIndex + 1} of {scrollPhases.length}</span><span>{manual ? "Select a feature" : "Scroll to explore"}</span></div>
    </div>
    <svg className="productExitBridge" width={bridge.width} height={bridge.height} viewBox={`0 0 ${bridge.width} ${Math.max(1,bridge.height)}`} aria-hidden="true" data-exiting={exiting}><path d={`M${bridge.x} 0 V${bridge.height}`} /></svg>
  </div>;
}
