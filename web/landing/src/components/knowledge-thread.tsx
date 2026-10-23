import { useEffect, useRef, useState, type RefObject } from "react";

type Point = { x: number; y: number };
type Scene = Point & { key: string; left: number; top: number; width: number; height: number; approach: Point[]; departure: Point[] };


export function KnowledgeThread({ journeyRef, revised }: { journeyRef: RefObject<HTMLDivElement | null>; revised: boolean }) {
  const [layout, setLayout] = useState<{ width: number; height: number; scenes: Scene[] }>({ width: 0, height: 0, scenes: [] });
  const overlay = useRef<SVGSVGElement>(null);
  const activePath = useRef<SVGPathElement>(null);
  const cursor = useRef<SVGCircleElement>(null);
  useEffect(() => {
    const journey = journeyRef.current;
    if (!journey) return;
    let frame = 0;
    let disposed = false;
    const measure = () => {
      const root = journey.getBoundingClientRect();
      const mobile = window.innerWidth <= 760;
      const scenes = Array.from(journey.querySelectorAll<HTMLElement>("[data-thread-scene]")).map(element => {
        const box = element.getBoundingClientRect();
        const key = element.dataset.threadScene!;
        const sceneX = box.left - root.left;
        const sceneY = box.top - root.top;
        const x = key === "mission" ? sceneX : ["connected", "scattered"].includes(key) ? 25 - root.left : key === "forward" ? sceneX + box.width * .5 : mobile ? 25 : sceneX + box.width * (key === "research" ? .7 : .5);
        const missionMatrix = key === "mission" ? element.querySelector("svg")?.getScreenCTM() : null;
        const missionPoint = missionMatrix ? new DOMPoint(0, 154).matrixTransform(missionMatrix) : null;
        const y = missionPoint ? missionPoint.y - root.top : key === "connected" ? sceneY : sceneY + box.height * (key === "beginning" ? .74 : .5);
        const copy = element.closest("section")?.querySelector(".journeyCopy")?.getBoundingClientRect();
        // Route through real whitespace, rather than hiding the thread beneath text masks.
        const approach: Point[] = [];
        const departure: Point[] = [];
        const section = element.closest("section")!.getBoundingClientRect();
        if (key === "scattered" && copy) {
          approach.push({ x: mobile ? 25 : root.width - 28, y: copy.top - root.top - 28 });
          approach.push({ x: mobile ? 25 : root.width - 28, y: sceneY + 5 });
        } else if (key === "connected") {
          approach.push({ x: 25 - root.left, y: section.top - root.top - 20 });
          departure.push({ x: 25 - root.left, y: section.bottom - root.top });
        } else if (key === "forward") {
          approach.push({ x: 25 - root.left, y: section.top - root.top + 70 });
          approach.push({ x: 25 - root.left, y: sceneY - 20 });
          approach.push({ x: sceneX + box.width * .14, y: sceneY + box.height * .16 });
          departure.push({ x: sceneX + box.width * .85, y: sceneY + box.height * .78 });
          departure.push({ x: mobile ? 25 : root.width - 28, y: section.bottom - root.top - 20 });
        } else if (key === "mission") {
          // The final connection is drawn as one continuous sweep below.
          // Extra waypoints here would flatten the curve into right-angle turns.
        } else if (key === "research") {
          approach.push({ x: mobile ? 25 : root.width - 28, y: section.top - root.top - 20 });
          departure.push({ x: mobile ? 25 : root.width - 28, y: section.bottom - root.top - 20 });
        }
        return { key, x, y, left: sceneX, top: sceneY, width: box.width, height: box.height, approach, departure };
      });
      setLayout({ width: root.width, height: root.height, scenes });
    };
    const scheduleMeasure = () => { if (disposed) return; cancelAnimationFrame(frame); frame = requestAnimationFrame(measure); };
    const observer = new ResizeObserver(scheduleMeasure);
    observer.observe(journey);
    journey.querySelectorAll(".journeyCopy, [data-thread-scene]").forEach(element => observer.observe(element));
    document.fonts.ready.then(scheduleMeasure);
    window.addEventListener("resize", scheduleMeasure);
    measure();
    return () => { disposed = true; observer.disconnect(); cancelAnimationFrame(frame); window.removeEventListener("resize", scheduleMeasure); };
  }, [journeyRef]);

  useEffect(() => {
    const journey = journeyRef.current;
    const path = activePath.current;
    if (!journey || !path || !layout.scenes.length) return;
    let frame = 0;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
    const length = path.getTotalLength();
    const documentTop = journey.getBoundingClientRect().top + window.scrollY;
    const groups = Array.from(overlay.current?.querySelectorAll<SVGGElement>(".threadNetwork") ?? []);
    path.style.strokeDasharray = `${length}`;
    const first = layout.scenes[0].y;
    const last = layout.scenes.at(-1)!.y;
    const update = () => {
      const localY = window.scrollY + window.innerHeight * .55 - documentTop;
      const progress = Math.min(1, Math.max(0, (localY - first) / (last - first)));
      path.style.strokeDashoffset = `${reduced.matches ? 0 : length * (1 - progress)}`;
      const point = path.getPointAtLength(progress * length);
      cursor.current?.setAttribute("cx", `${point.x}`);
      cursor.current?.setAttribute("cy", `${point.y}`);
      cursor.current?.setAttribute("opacity", reduced.matches || localY < first - 120 || localY > last + 250 ? "0" : "1");
      groups.forEach((group, index) => {
        const reached = reduced.matches || localY + window.innerHeight * .4 > layout.scenes[index].y ? "true" : "false";
        if (group.dataset.reached !== reached) group.dataset.reached = reached;
      });
    };
    const onScroll = () => { if (!frame) frame = requestAnimationFrame(() => { frame = 0; update(); }); };
    window.addEventListener("scroll", onScroll, { passive: true });
    reduced.addEventListener("change", update);
    update();
    return () => { window.removeEventListener("scroll", onScroll); reduced.removeEventListener("change", update); cancelAnimationFrame(frame); };
  }, [layout, journeyRef]);

  if (!layout.scenes.length) return null;
  const route: (Point & { mission?: boolean })[] = layout.scenes.flatMap(scene => [...scene.approach, { x: scene.x, y: scene.y, mission: scene.key === "mission" }, ...scene.departure]);
  const d = route.map((point, index, all) => {
    if (!index) return `M${point.x},${point.y}`;
    const previous = all[index - 1];
    if (point.mission) {
      const span = point.y - previous.y;
      const rail = Math.min(25, point.x - 20);
      const turnY = previous.y + span * .64;
      if (layout.width <= 760) return `C${previous.x},${previous.y + span * .4} ${rail},${turnY} ${rail},${turnY} C${rail},${point.y} ${point.x - 20},${point.y} ${point.x},${point.y}`;
      return `C${previous.x},${previous.y + span * .26} ${previous.x - 35},${previous.y + span * .26} ${previous.x - 110},${previous.y + span * .32} C${previous.x - 210},${previous.y + span * .4} ${rail},${previous.y + span * .38} ${rail},${turnY} C${rail},${point.y} ${point.x - 20},${point.y} ${point.x},${point.y}`;
    }
    const gap = (point.y - previous.y) * .45;
    return `C${previous.x},${previous.y + gap} ${point.x},${point.y - gap} ${point.x},${point.y}`;
  }).join(" ");
  return <svg ref={overlay} className="knowledgeThread" width={layout.width} height={layout.height} viewBox={`0 0 ${layout.width} ${layout.height}`} aria-hidden="true">
    <path className="threadSpine" d={d} />
    <path ref={activePath} className="threadSpine threadSpineActive" d={d} />
    {layout.scenes.map(scene => {
      const mobile = layout.width <= 760;
      const centerX = mobile ? scene.left + scene.width * .5 : scene.x;
      const centerY = scene.y;
      const left = scene.left, top = scene.top, w = scene.width, h = scene.height;
      let artwork;
      if (scene.key === "beginning") {
        artwork = <g className="sceneLine"><path className="networkEdge sceneSweep" d={`M${left + w * .12},${top + h * .04} C${left + w * .4},${top - h * .1} ${left + w * .96},${top - h * .1} ${left + w * .96},${top + h * .08} C${left + w * 1.02},${top + h * .45} ${left + w * 1.02},${top + h * .95} ${left + w * .8},${top + h * .95} C${left + w * .65},${top + h * .95} ${left + w * .63},${centerY} ${centerX},${centerY}`} /><circle className="networkCoreOuter" cx={centerX} cy={centerY} r="17" /><circle className="networkCore" cx={centerX} cy={centerY} r="6" /></g>;
      } else if (["scattered", "connected"].includes(scene.key)) {
        artwork = null;
      } else if (scene.key === "forward") {
        const a = {x: left + w * .14, y: top + h * .16};
        const b = {x: left + w * .85, y: top + h * .78};
        artwork = <g className="sceneBranch"><circle className="networkNode" cx={a.x} cy={a.y} r="6" /><circle className="networkCoreOuter" cx={centerX} cy={centerY} r="15" /><circle className="networkCore" cx={centerX} cy={centerY} r="7" /><circle className="networkNode" cx={b.x} cy={b.y} r="6" /><text x={a.x} y={a.y - 17}>Your finding</text><text x={centerX} y={centerY + 35} textAnchor="middle">Shared knowledge</text><text x={b.x} y={b.y + 27} textAnchor="end">The next experiment</text></g>;
      } else if (scene.key === "changing") {
        artwork = <g className="sceneRevision"><path className="networkEdge" d={`M${left},${centerY} Q${centerX - w * .15},${centerY + h * .3} ${centerX},${centerY} T${left + w},${centerY}`} /><circle className={revised ? "networkQuestion" : "networkCore"} cx={centerX} cy={centerY} r="6" /></g>;
      } else {
        // The primary path owns this connection; no decorative parallel route.
        artwork = null;
      }
      return <g key={scene.key} className={`threadNetwork network-${scene.key}`} data-reached="true">{mobile && ["beginning"].includes(scene.key) && <path className="networkBridge" d={`M${scene.x},${scene.y} Q${(scene.x + centerX) / 2},${scene.y + 42} ${centerX},${scene.y}`} />}{artwork}</g>;
    })}
    <circle ref={cursor} className="threadCursor" r="7" />
  </svg>;
}
