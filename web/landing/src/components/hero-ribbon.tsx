export function HeroRibbon() {
  return (
    <div className="heroRibbon" aria-hidden="true">
      <svg viewBox="0 0 620 720" focusable="false">
        <defs>
          <linearGradient id="ribbon-stroke" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#8fd0d8" stopOpacity="0.12" />
            <stop offset="0.48" stopColor="#26a2b3" stopOpacity="0.72" />
            <stop offset="1" stopColor="#0e6675" stopOpacity="0.95" />
          </linearGradient>
          <filter id="ribbon-soft" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="16" />
          </filter>
        </defs>

        <path className="ribbonGlow" d="M34 590C170 566 198 420 298 370C400 318 436 214 585 116" />
        <path className="ribbonStrand ribbonStrandA" d="M20 622C174 592 190 442 298 378C404 316 450 226 596 132" />
        <path className="ribbonStrand ribbonStrandB" d="M18 560C158 556 216 416 300 374C394 326 432 194 576 78" />
        <path className="ribbonCore" d="M22 592C166 576 206 428 300 374C398 318 444 210 588 106" />

        <g className="ribbonGate">
          <circle cx="300" cy="374" r="24" />
          <circle cx="300" cy="374" r="6" />
        </g>
        <g className="ribbonParticles">
          <circle cx="92" cy="551" r="3" />
          <circle cx="132" cy="594" r="4" />
          <circle cx="179" cy="492" r="3" />
          <circle cx="214" cy="454" r="4" />
          <circle cx="462" cy="244" r="3" />
          <circle cx="516" cy="168" r="4" />
        </g>
      </svg>
    </div>
  );
}
