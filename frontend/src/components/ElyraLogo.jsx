export default function ElyraLogo({ className = 'h-8 w-8', showText = false, showSubtitle = false, textClass = 'h-5' }) {
  return (
    <div className="flex items-center gap-4 select-none">
      {/* Symbol Mark SVG */}
      <svg
        viewBox="0 0 100 100"
        className={className}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          {/* Silver/White Tapered Spine Gradient */}
          <linearGradient id="silverSpineGradient" x1="20" y1="15" x2="64" y2="85" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#E4E4E7" />
            <stop offset="20%" stopColor="#FAFAFA" />
            <stop offset="50%" stopColor="#FFFFFF" />
            <stop offset="80%" stopColor="#E4E4E7" />
            <stop offset="100%" stopColor="#A1A1AA" />
          </linearGradient>

          {/* Purple Wave Gradient */}
          <linearGradient id="purpleWaveGradient" x1="10" y1="50" x2="68" y2="44" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#D8B4FE" />   {/* Light Lavender */}
            <stop offset="50%" stopColor="#C084FC" />  {/* Lavender Purple */}
            <stop offset="100%" stopColor="#818CF8" /> {/* Indigo Blue base for star */}
          </linearGradient>

          {/* Radial Shine/Spotlight Glow */}
          <radialGradient id="spotlightGlow" cx="22" cy="50" r="16" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="1" />
            <stop offset="25%" stopColor="#E9D5FF" stopOpacity="0.8" />
            <stop offset="60%" stopColor="#C084FC" stopOpacity="0.25" />
            <stop offset="100%" stopColor="#C084FC" stopOpacity="0" />
          </radialGradient>

          {/* Wordmark Star Gradient */}
          <linearGradient id="starGradient" x1="102" y1="12" x2="106" y2="16" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#E2D5FA" />
            <stop offset="100%" stopColor="#C084FC" />
          </linearGradient>
        </defs>

        {/* 1. Ambient Background Glow at the crossover point */}
        <circle cx="22" cy="50" r="18" fill="url(#spotlightGlow)" opacity="0.65" />

        {/* 2. Outer C-backbone (Substantial thickness: sweeps from narrow ends to a bold center spine) */}
        <path
          d="M 64,15 C 32,15 16,28 16,50 C 16,72 32,85 64,85 V 83 C 34,83 28,70 28,50 C 28,30 34,17 64,17 Z"
          fill="url(#silverSpineGradient)"
        />

        {/* 3. Horizontal Wave (Overlap, curves through backbone) */}
        <path
          d="M 10,60 C 20,52 20,44 26,44 C 34,44 44,53 52,53 C 60,53 64,48 68,44 C 64,47 52,56 44,56 C 36,56 26,48 10,60 Z"
          fill="url(#purpleWaveGradient)"
        />

        {/* 4. Active Shining Crossover Spotlight (Layered flare highlight) */}
        <circle cx="22" cy="50" r="8" fill="url(#spotlightGlow)" opacity="0.95" />

        {/* 5. 4-point star on the wave tip */}
        <path
          d="M 68,27 Q 68,36 60,36 Q 68,36 68,45 Q 68,36 76,36 Q 68,36 68,27 Z"
          fill="url(#purpleWaveGradient)"
        />
      </svg>

      {/* Wordmark E L Y R A */}
      {showText && (
        <div className="flex flex-col justify-center text-left">
          <svg
            viewBox="0 0 114 20"
            className={`${textClass} w-auto text-white`}
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Letter E */}
            <path
              d="M 12,0.5 H 0.5 V 19.5 H 12 M 0.5,10 H 9.5"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* Letter L */}
            <path
              d="M 24,0.5 V 19.5 H 35.5"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* Letter Y */}
            <path
              d="M 46.5,0.5 L 54,10 V 19.5 M 61.5,0.5 L 54,10"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* Letter R */}
            <path
              d="M 72.5,19.5 V 0.5 H 81.5 C 85,0.5 86.5,2.5 86.5,5.5 C 86.5,8.5 85,10 81.5,10 H 72.5 M 79.5,10 L 86.5,19.5"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* Letter A (without crossbar) */}
            <path
              d="M 96.5,19.5 L 104,0.5 L 111.5,19.5"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* Star inside Letter A */}
            <path
              d="M 104,11.5 Q 104,14 101.5,14 Q 104,14 104,16.5 Q 104,14 106.5,14 Q 104,14 104,11.5 Z"
              fill="url(#starGradient)"
            />
          </svg>
          {showSubtitle && (
            <span className="text-[7.5px] tracking-[0.24em] text-text-muted font-bold mt-1.5 uppercase leading-none">
              Understand beyond words
            </span>
          )}
        </div>
      )}
    </div>
  )
}
