// ============================================================================
// RAGAS EVALUATION PANEL
// ============================================================================
// Displays RAGAS evaluation metrics showing the quality of the RAG pipeline.
// ============================================================================

export default function RagasPanel({ results }) {
  if (!results || !results.summary) {
    return null;
  }

  const { summary, details } = results;
  const hasResults = summary.faithfulness > 0 || summary.answer_relevancy > 0 || 
                     summary.context_precision > 0 || summary.context_recall > 0;

  // Color coding for scores: red < 0.5, yellow 0.5-0.7, green > 0.7
  const getScoreColor = (score) => {
    if (score < 0.5) return "text-red-600";
    if (score < 0.7) return "text-yellow-600";
    return "text-green-600";
  };

  const getScoreBgColor = (score) => {
    if (score < 0.5) return "bg-red-50";
    if (score < 0.7) return "bg-yellow-50";
    return "bg-green-50";
  };

  return (
    <div className="border-t border-gray-200 pt-4 mt-4">
      <h3 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
      </h3>

      {!hasResults ? (
        <p className="text-sm text-gray-500">
        </p>
      ) : (
        <>
          {/* Summary Scores */}
          <div className="grid grid-cols-2 gap-2 mb-4">
            <div className={`p-3 rounded border border-gray-200 ${getScoreBgColor(summary.faithfulness)}`}>
              <div className="text-xs font-medium text-gray-600">Faithfulness</div>
              <div className={`text-lg font-bold ${getScoreColor(summary.faithfulness)}`}>
                {(summary.faithfulness)}%
              </div>
            </div>

            <div className={`p-3 rounded border border-gray-200 ${getScoreBgColor(summary.answer_relevancy)}`}>
              <div className="text-xs font-medium text-gray-600">Answer Relevancy</div>
              <div className={`text-lg font-bold ${getScoreColor(summary.answer_relevancy)}`}>
                {(summary.answer_relevancy)}%
              </div>
            </div>

            <div className={`p-3 rounded border border-gray-200 ${getScoreBgColor(summary.context_precision)}`}>
              <div className="text-xs font-medium text-gray-600">Context Precision</div>
              <div className={`text-lg font-bold ${getScoreColor(summary.context_precision)}`}>
                {(summary.context_precision)}%
              </div>
            </div>

            <div className={`p-3 rounded border border-gray-200 ${getScoreBgColor(summary.context_recall)}`}>
              <div className="text-xs font-medium text-gray-600">Context Recall</div>
              <div className={`text-lg font-bold ${getScoreColor(summary.context_recall)}`}>
                {(summary.context_recall)}%
              </div>
            </div>
          </div>

          {/* Metric Descriptions */}
          <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-3">
            <p className="text-xs text-gray-700">
              <strong>Faithfulness:</strong> Is the answer factually grounded in retrieved context?<br/>
              <strong>Answer Relevancy:</strong> Does the answer address the question?<br/>
              <strong>Context Precision:</strong> How much retrieved context is relevant?<br/>
              <strong>Context Recall:</strong> Did retrieval find everything needed to answer?
            </p>
          </div>

          {/* Individual Questions */}
          {details && details.length > 0 && (
            <div>
              <h4 className="font-medium text-gray-700 text-sm mb-2">Per-Question Scores</h4>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {details.map((detail, idx) => (
                  <div key={idx} className="bg-gray-50 p-2 rounded text-xs border border-gray-200">
                    <p className="font-medium text-gray-700 mb-1 truncate">{detail.question}</p>
                    <div className="grid grid-cols-2 gap-1">
                      <div className="text-gray-600">
                        Faithfulness: <span className={getScoreColor(detail.faithfulness)}>
                          {(detail.faithfulness)}%
                        </span>
                      </div>
                      <div className="text-gray-600">
                        Relevancy: <span className={getScoreColor(detail.answer_relevancy)}>
                          {(detail.answer_relevancy)}%
                        </span>
                      </div>
                      <div className="text-gray-600">
                        Precision: <span className={getScoreColor(detail.context_precision)}>
                          {(detail.context_precision)}%
                        </span>
                      </div>
                      <div className="text-gray-600">
                        Recall: <span className={getScoreColor(detail.context_recall)}>
                          {(detail.context_recall)}%
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
