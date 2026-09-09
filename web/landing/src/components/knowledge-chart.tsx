export function KnowledgeChart() {
  return (
    <figure className="knowledgeFigure" aria-describedby="knowledge-chart-note">
      <svg
        className="knowledgeChart knowledgeChartDesktop"
        viewBox="0 0 1200 650"
        role="img"
        aria-labelledby="knowledge-chart-title knowledge-chart-description"
      >
        <title id="knowledge-chart-title">Agent output outgrows the organization’s verification capacity</title>
        <desc id="knowledge-chart-description">
          An illustrative curve shows agent-produced knowledge growing faster than the intelligence
          retained by the organization as agent autonomy increases. A marked point shows where output
          exceeds the organization’s existing verification capacity.
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
          <text x="426" y="242" className="chartLabel chartLabelStrong">OUTPUT EXCEEDS VERIFICATION CAPACITY</text>
        </g>

        <text x="1000" y="94" className="curveLabel agentLabel">
          <tspan x="1000" dy="0">Agent-produced</tspan>
          <tspan x="1000" dy="31">knowledge</tspan>
        </text>
        <text x="850" y="326" className="curveLabel enterpriseLabel">Organization-owned intelligence</text>
        <text x="610" y="620" textAnchor="middle" className="axisLabel">Agent adoption and autonomy over time</text>
        <text x="42" y="310" textAnchor="middle" transform="rotate(-90 42 310)" className="axisLabel">Reusable claims and work</text>
      </svg>
      <svg
        className="knowledgeChart knowledgeChartMobile"
        viewBox="0 0 360 500"
        role="img"
        aria-labelledby="knowledge-chart-mobile-title knowledge-chart-mobile-description"
      >
        <title id="knowledge-chart-mobile-title">Agent output outgrows the organization’s verification capacity</title>
        <desc id="knowledge-chart-mobile-description">
          An illustrative mobile chart shows agent-produced knowledge rising faster than intelligence
          retained by the organization, with a marked point where output exceeds verification capacity.
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
          <text x="128" y="246" className="chartLabel chartLabelStrong">
            <tspan x="128" dy="0">OUTPUT EXCEEDS</tspan>
            <tspan x="128" dy="18">VERIFICATION CAPACITY</tspan>
          </text>
        </g>
        <text x="186" y="470" textAnchor="middle" className="axisLabel">More agent autonomy →</text>
      </svg>
      <div className="mobileChartLegend" aria-hidden="true">
        <span><i className="agentSwatch" />Agent-produced knowledge</span>
        <span><i className="enterpriseSwatch" />Organization-owned intelligence</span>
      </div>
      <figcaption id="knowledge-chart-note">
        Illustrative model — not measured data. Without a trusted learning loop, the gap keeps widening.
      </figcaption>
    </figure>
  );
}
