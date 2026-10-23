import { useEffect, useRef, useState, useId } from "react";
import "./knowledge-confluence.css";

// Authored channels gather at a common inlet, then form a larger connected body.
const channels = [40, 94, 150, 211, 267];
const nodes = Array.from({ length: 9 }, (_, column) => Array.from({ length: column < 2 ? 3 : 7 }, (_, row) => {
  const spread = 28 + column * 9;
  const count = column < 2 ? 3 : 7;
  return { x: 415 + column * 78 + (row % 2) * 13, y: 154 + (row - (count - 1) / 2) * spread / (count < 4 ? 1 : 2), column, row };
})).flat();

export function KnowledgeConfluence() {
  const root = useRef<HTMLDivElement>(null);
  const clipId = useId();
  const [entered, setEntered] = useState(false);
  const [visible, setVisible] = useState(false);
  const [replay, setReplay] = useState(0);
  useEffect(() => {
    const element = root.current;
    if (!element) return;
    const observer = new IntersectionObserver(([entry]) => { setVisible(entry.isIntersecting); if (entry.isIntersecting) setEntered(true); }, { threshold: .25 });
    const visibility = () => { const box = root.current?.getBoundingClientRect(); setVisible(!document.hidden && !!box && box.bottom > 0 && box.top < window.innerHeight); };
    observer.observe(element); document.addEventListener("visibilitychange", visibility);
    return () => { observer.disconnect(); document.removeEventListener("visibilitychange", visibility); };
  }, []);
  return <div ref={root} className="knowledgeConfluence" data-thread-scene="mission" data-entered={entered} data-visible={visible}>
    <svg viewBox="0 0 1100 330" aria-hidden="true" key={replay}>
      <defs><clipPath id={clipId}><rect className="confluenceRevealWindow" x="0" y="0" width="1100" height="330" /></clipPath></defs>
      <g clipPath={`url(#${clipId})`}>
        <g className="confluenceStreams">{channels.map(y => <path key={y} d={`M0 ${y} C145 ${y} 177 ${154 + (y - 154) * .1} 415 154`} />)}</g>
        <path className="confluenceCurrent" d="M0 154 H1100" />
        {nodes.map((node, index) => {
          const previous = nodes.filter(n => n.column === node.column - 1);
          const parent = previous.length ? previous.reduce((a,b) => Math.abs(a.y - node.y) < Math.abs(b.y - node.y) ? a : b) : { x: 360, y: 154 };
          return <g key={index} className="confluenceBranch">
            <path d={`M${parent.x} ${parent.y} C${parent.x + 38} ${parent.y} ${node.x - 38} ${node.y} ${node.x} ${node.y}`} />
            <circle cx={node.x} cy={node.y} r={node.row === 3 || (node.column < 2 && node.row === 1) ? 5 : 2.8} className={node.row === 3 ? "confluenceCore" : ""} />
          </g>;
        })}
      </g>
      <g className="confluenceTraveller"><circle cx="0" cy="154" r="9" className="confluenceTravellerSurface" /><circle cx="0" cy="154" r="6" /></g>
    </svg>
    <div className="confluenceFoot"><button type="button" onClick={() => setReplay(current => current + 1)}>Replay</button></div>
  </div>;
}
