export function KnowledgeChart() {
  return (
    <figure className="knowledgeFigure" aria-describedby="knowledge-chart-note">
      <svg
        className="knowledgeChart knowledgeChartDesktop"
        viewBox="0 0 1200 650"
        role="img"
        aria-labelledby="knowledge-chart-title knowledge-chart-description"
      >
        <title id="knowledge-chart-title">Agent-produced findings outpace verified organizational knowledge</title>
        <desc id="knowledge-chart-description">
          Conceptual curves compare accumulated agent-produced findings with verified organizational
          knowledge over time. The widening gap represents unverified findings, not measured growth rates.
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

        <path className="enterpriseCurve" d="M122 516L760 420" />
        <path className="agentCurve" d="M122 516C450 480 725 455 760 96" />

        <g className="threshold">
          <path d="M800 112V420M788 112H812M788 420H812" />
          <text x="842" y="276" className="curveLabel agentLabel">Unverified findings</text>
        </g>

        <text x="842" y="106" className="curveLabel agentLabel">
          <tspan x="842" dy="0">Agent-produced</tspan>
          <tspan x="842" dy="31">findings</tspan>
        </text>
        <text x="842" y="420" className="curveLabel enterpriseLabel"><tspan x="842">Verified organizational</tspan><tspan x="842" dy="31">knowledge</tspan></text>
        <text x="1058" y="604" className="axisLabel">Time</text>
        <text x="120" y="36" className="axisLabel">Accumulated findings</text>
      </svg>
      <svg
        className="knowledgeChart knowledgeChartMobile"
        viewBox="0 0 360 500"
        role="img"
        aria-labelledby="knowledge-chart-mobile-title knowledge-chart-mobile-description"
      >
        <title id="knowledge-chart-mobile-title">Agent findings outpace verified organizational knowledge</title>
        <desc id="knowledge-chart-mobile-description">
          Conceptual curves show agent findings rising faster than verified organizational knowledge.
          The bracket marks the widening gap of unverified findings. These are not measured growth rates.
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
        <path className="enterpriseCurve" d="M44 402L270 340" />
        <path className="agentCurve" d="M44 402C210 372 260 345 270 72" />
        <g className="threshold">
          <path d="M300 88V340M292 88H308M292 340H308" />
          <text x="68" y="170" className="chartLabel chartLabelStrong">
            <tspan x="68" dy="0">Unverified</tspan>
            <tspan x="68" dy="23">findings</tspan>
          </text>
        </g>
        <text x="42" y="24" className="axisLabel">Accumulated findings</text>
        <text x="300" y="470" className="axisLabel">Time</text>
      </svg>
      <div className="mobileChartLegend" aria-hidden="true">
        <span><i className="agentSwatch" />Agent-produced findings</span>
        <span><i className="enterpriseSwatch" />Verified organizational knowledge</span>
      </div>
      <figcaption id="knowledge-chart-note">
        Illustrative model
      </figcaption>
    </figure>
  );
}
