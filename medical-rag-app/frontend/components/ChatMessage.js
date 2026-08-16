// ============================================================================
// CHAT MESSAGE
// ----------------------------------------------------------------------------
// One bubble in the conversation. Assistant messages can carry a list of
// source chunks, shown as small citation chips under the answer.
// Also displays RAGAS quality metrics for assistant responses.
// ============================================================================

export default function ChatMessage({ role, text, sources, pending, ragas }) {
  const isUser = role === "user";

  const getScoreColor = (score) => {
    if (score < 0.5) return "text-red-600";
    if (score < 0.7) return "text-yellow-600";
    return "text-green-600";
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[640px] px-4 py-3.5 rounded-2xl text-[14.5px] leading-relaxed whitespace-pre-wrap ${
          isUser
            ? "bg-teal-700 text-white rounded-tr-sm"
            : `bg-surface border border-border text-ink rounded-tl-sm ${pending ? "italic text-ink-soft" : ""}`
        }`}
      >
        {text}

        {sources && sources.length > 0 && (
          <div className="mt-2.5 pt-2.5 border-t border-dashed border-border flex flex-col gap-1.5">
            {sources.map((s, i) => (
              <span
                key={i}
                className="font-mono text-[11px] text-teal-700 bg-teal-100 px-2 py-1 rounded-md w-fit"
              >
                {s.document} · p.{s.page ?? "?"}
              </span>
            ))}
          </div>
        )}

        {ragas && !pending && (
          <div className="mt-2.5 pt-2.5 border-t border-dashed border-border">
            <div className="text-[11px] font-semibold text-ink-soft mb-1.5">📊 Quality Metrics</div>
            <div className="grid grid-cols-2 gap-1.5">
              <div className="bg-blue-50 px-2 py-1 rounded text-[11px]">
                <div className="text-ink-soft">Faithfulness</div>
                <div className={`font-bold ${getScoreColor(ragas.faithfulness)}`}>
                  {(ragas.faithfulness * 100).toFixed(0)}%
                </div>
              </div>
              <div className="bg-blue-50 px-2 py-1 rounded text-[11px]">
                <div className="text-ink-soft">Answer Relevancy</div>
                <div className={`font-bold ${getScoreColor(ragas.answer_relevancy)}`}>
                  {(ragas.answer_relevancy * 100).toFixed(0)}%
                </div>
              </div>
              <div className="bg-blue-50 px-2 py-1 rounded text-[11px]">
                <div className="text-ink-soft">Context Precision</div>
                <div className={`font-bold ${getScoreColor(ragas.context_precision)}`}>
                  {(ragas.context_precision * 100).toFixed(0)}%
                </div>
              </div>
              <div className="bg-blue-50 px-2 py-1 rounded text-[11px]">
                <div className="text-ink-soft">Context Recall</div>
                <div className={`font-bold ${getScoreColor(ragas.context_recall)}`}>
                  {(ragas.context_recall * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
