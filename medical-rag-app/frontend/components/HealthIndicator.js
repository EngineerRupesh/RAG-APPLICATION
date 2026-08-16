// ============================================================================
// HEALTH INDICATOR
// ----------------------------------------------------------------------------
// Small pill in the header showing whether the backend + index are reachable.
// `health` is null while loading, an object on success, or "down" on failure.
// ============================================================================

export default function HealthIndicator({ health }) {
  const isDown = health === "down";
  const isLoading = health === null;

  const dotClass = isLoading
    ? "bg-[#c4c4c4]"
    : isDown
    ? "bg-[#c0392b] shadow-[0_0_0_3px_rgba(192,57,43,0.2)]"
    : "bg-[#2e9e5f] shadow-[0_0_0_3px_rgba(46,158,95,0.2)]";

  const label = isLoading
    ? "Checking…"
    : isDown
    ? "Backend unreachable"
    : `${health.indexed_documents} doc(s) · ${health.llm_provider}`;

  return (
    <div className="flex items-center gap-2 font-mono text-xs text-ink-soft px-3 py-1.5 border border-border rounded-full bg-teal-100">
      <span className={`w-2 h-2 rounded-full transition-colors ${dotClass}`} />
      <span>{label}</span>
    </div>
  );
}
