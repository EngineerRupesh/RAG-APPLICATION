// ============================================================================
// HEADER
// ----------------------------------------------------------------------------
// Brand mark (with the app's signature animated ECG trace) on the left,
// live backend health status on the right.
// ============================================================================

import HealthIndicator from "./HealthIndicator";

export default function Header({ health }) {
  return (
    <header className="flex items-center justify-between px-7 py-3.5 bg-surface border-b border-border shrink-0">
      <div className="flex items-center gap-3.5">
        {/* Signature ECG trace mark - the visual motif of the whole app */}
        <svg className="w-[100px] h-7" viewBox="0 0 120 32" aria-hidden="true">
          <path
            className="ecg-path animate-draw-ecg"
            d="M0 16 H28 L34 4 L42 28 L48 16 H62 L67 10 L72 22 L77 16 H120"
            fill="none"
            stroke="#2e9e8f"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeDasharray="220"
          />
        </svg>
        <div>
          <h1 className="font-display font-bold text-xl text-teal-900 tracking-tight leading-tight">
            MedGrounded
          </h1>
          <p className="text-xs text-ink-soft leading-tight">
            Answers grounded in your uploaded documents
          </p>
        </div>
      </div>

      <HealthIndicator health={health} />
    </header>
  );
}
