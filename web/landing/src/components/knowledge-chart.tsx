export function KnowledgeChart() {
  return (
    <figure className="knowledgeFigure" aria-describedby="knowledge-chart-note">
      <svg
        className="knowledgeChart knowledgeChartDesktop"
        viewBox="0 0 1200 650"
        role="img"
        aria-labelledby="knowledge-chart-title knowledge-chart-description"
      >
        <title id="knowledge-chart-title">Agent-produced knowledge creates a governance threshold</title>
        <desc id="knowledge-chart-description">
          An illustrative curve shows agent-produced knowledge growing faster than traditional
          enterprise knowledge as agent autonomy increases. A marked threshold shows where
          outputs become durable inputs and governance becomes necessary.
        </desc>
        <defs>
          <marker id="axis-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" />
          </marker>
          <marker id="teal-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" />
          </marker>
        </defs>

        <g className="chartAxes">
          <path d="M120 548V66" markerEnd="url(#axis-arrow)" />
          <path d="M120 548H1110" markerEnd="url(#axis-arrow)" />
        </g>

        <path className="enterpriseCurve" d="M122 516C330 455 620 390 1054 346" markerEnd="url(#axis-arrow)" />
        <path className="agentCurve" d="M122 516C420 451 700 397 820 284C905 204 952 123 984 62" markerEnd="url(#teal-arrow)" />

        <g className="threshold">
          <path d="M744 548V348" />
          <circle cx="744" cy="348" r="5" />
          <path className="thresholdLeader" d="M584 260L730 337" markerEnd="url(#teal-arrow)" />
          <text x="426" y="228" className="chartLabel chartLabelStrong">GOVERNANCE THRESHOLD</text>
          <text x="426" y="255" className="chartAnnotation">When outputs become durable inputs</text>
        </g>

        <text x="1000" y="94" className="curveLabel agentLabel">
          <tspan x="1000" dy="0">Agent-produced</tspan>
          <tspan x="1000" dy="31">knowledge</tspan>
        </text>
        <text x="890" y="326" className="curveLabel enterpriseLabel">Enterprise knowledge</text>
        <text x="610" y="620" textAnchor="middle" className="axisLabel">Agent adoption and autonomy over time</text>
        <text x="42" y="310" textAnchor="middle" transform="rotate(-90 42 310)" className="axisLabel">Reusable conclusions and work</text>
      </svg>
      <svg
        className="knowledgeChart knowledgeChartMobile"
        viewBox="0 0 360 500"
        role="img"
        aria-labelledby="knowledge-chart-mobile-title knowledge-chart-mobile-description"
      >
        <title id="knowledge-chart-mobile-title">Agent-produced knowledge creates a governance threshold</title>
        <desc id="knowledge-chart-mobile-description">
          An illustrative mobile chart shows agent-produced knowledge rising faster than enterprise
          knowledge, with a governance threshold where outputs become durable inputs.
        </desc>
        <defs>
          <marker id="mobile-axis-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" />
          </marker>
          <marker id="mobile-teal-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" />
          </marker>
        </defs>
        <g className="chartAxes">
          <path d="M42 430V44" markerEnd="url(#mobile-axis-arrow)" />
          <path d="M42 430H330" markerEnd="url(#mobile-axis-arrow)" />
        </g>
        <path className="enterpriseCurve" d="M44 402C132 356 224 322 310 300" markerEnd="url(#mobile-axis-arrow)" />
        <path className="agentCurve" d="M44 402C148 354 212 315 246 249C275 192 292 126 301 65" markerEnd="url(#mobile-teal-arrow)" />
        <g className="threshold">
          <path d="M220 430V291" />
          <circle cx="220" cy="291" r="4" />
          <text x="128" y="245" className="chartLabel chartLabelStrong">GOVERNANCE</text>
          <text x="128" y="260" className="chartLabel chartLabelStrong">THRESHOLD</text>
          <text x="128" y="278" className="chartAnnotation">Outputs become inputs</text>
        </g>
        <text x="220" y="94" className="curveLabel agentLabel">
          <tspan x="220" dy="0">Agent-produced</tspan>
          <tspan x="220" dy="17">knowledge</tspan>
        </text>
        <text x="196" y="326" className="curveLabel enterpriseLabel">Enterprise knowledge</text>
        <text x="186" y="470" textAnchor="middle" className="axisLabel">Agent adoption and autonomy over time</text>
        <text x="13" y="240" textAnchor="middle" transform="rotate(-90 13 240)" className="axisLabel">Reusable conclusions and work</text>
      </svg>
      <figcaption id="knowledge-chart-note">
        Illustrative model — not measured data. The threshold is organizational: the point where
        agent output starts becoming a premise for consequential downstream work.
      </figcaption>
    </figure>
  );
}
