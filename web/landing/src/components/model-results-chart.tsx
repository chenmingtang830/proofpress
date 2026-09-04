const modelResults = [
  { model: "Claude Opus 4.8", ordinary: 87.85211267605634, proofpress: 96.0093896713615 },
  { model: "Qwen 3.8 27B", ordinary: 89.02582159624414, proofpress: 93.83802816901408 },
  { model: "GLM 5.2", ordinary: 88.43896713615024, proofpress: 92.54694835680752 },
  { model: "GPT-5.6 SOL", ordinary: 89.26056338028168, proofpress: 93.25117370892019 },
  { model: "Muse Spark 1.1", ordinary: 91.90140845070422, proofpress: 95.71596244131455 },
  { model: "DeepSeek V4 Flash", ordinary: 89.08450704225352, proofpress: 92.25352112676056 },
  { model: "Inkling", ordinary: 89.67136150234741, proofpress: 90.19953051643192 },
];

const scaleFloor = 75;
const scaleRange = 100 - scaleFloor;
const scaleWidth = (value: number) =>
  `${Math.max(0, Math.min(100, ((value - scaleFloor) / scaleRange) * 100))}%`;

export function ModelResultsChart() {
  return (
    <figure className="modelChart" aria-labelledby="model-chart-title model-chart-caption">
      <div className="modelChartHead">
        <h3 id="model-chart-title">Rubric completion by model</h3>
        <div className="modelLegend" aria-label="Series legend">
          <span><i className="ordinarySwatch" />Ordinary</span>
          <span><i className="proofpressSwatch" />Proofpress</span>
        </div>
      </div>

      <div className="modelScale" aria-hidden="true">
        <span>75</span><span>80</span><span>85</span><span>90</span><span>95</span><span>100%</span>
      </div>

      <div className="modelRows">
        {modelResults.map((result) => {
          const delta = (result.proofpress - result.ordinary).toFixed(1);
          const description = `${result.model}: ordinary ${result.ordinary.toFixed(1)} percent, Proofpress ${result.proofpress.toFixed(1)} percent, an improvement of ${delta} percentage points.`;

          return (
            <div className="modelResult" key={result.model} aria-label={description}>
              <div className="modelResultLabel">
                <span>{result.model}</span>
                <strong>+{delta} pp</strong>
              </div>
              <div className="modelBarPair" aria-hidden="true">
                <div className="modelTrack">
                  <div className="modelBar ordinaryBar" style={{ width: scaleWidth(result.ordinary) }}>
                    <span>{result.ordinary.toFixed(1)}</span>
                  </div>
                </div>
                <div className="modelTrack">
                  <div className="modelBar proofpressBar" style={{ width: scaleWidth(result.proofpress) }}>
                    <span>{result.proofpress.toFixed(1)}</span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <figcaption id="model-chart-caption">
        Seven complete frozen panels, 18 paired runs per model. Ordered by uplift; zoomed 75–100% scale.
      </figcaption>
    </figure>
  );
}
