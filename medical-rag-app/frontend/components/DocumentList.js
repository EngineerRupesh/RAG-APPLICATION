// ============================================================================
// DOCUMENT LIST
// ----------------------------------------------------------------------------
// Renders the currently indexed documents, each with a delete (✕) button.
// Deletion state (which doc is mid-delete) is tracked here so only that
// row's button disables, not the whole list.
// ============================================================================

"use client";

import { useState } from "react";

export default function DocumentList({ documents, onDelete }) {
  const [deletingId, setDeletingId] = useState(null);

  async function handleDelete(docId) {
    setDeletingId(docId);
    try {
      await onDelete(docId);
    } finally {
      setDeletingId(null);
    }
  }

  if (documents.length === 0) {
    return <p className="text-sm text-ink-soft italic">No documents uploaded yet.</p>;
  }

  return (
    <ul className="flex flex-col gap-2">
      {documents.map((doc) => (
        <li
          key={doc.doc_id}
          className="flex items-center justify-between gap-2 px-3 py-2.5 border border-border rounded-xl bg-bg"
        >
          <div className="min-w-0">
            <div className="text-sm font-semibold text-ink truncate" title={doc.filename}>
              {doc.filename}
            </div>
            <div className="font-mono text-[11px] text-ink-soft">
              {doc.num_chunks} chunks · {new Date(doc.uploaded_at).toLocaleString()}
            </div>
          </div>

          <button
            type="button"
            title="Delete this document"
            disabled={deletingId === doc.doc_id}
            onClick={() => handleDelete(doc.doc_id)}
            className="shrink-0 text-red-700 text-base leading-none p-1.5 rounded-lg hover:bg-red-50 disabled:opacity-40 disabled:cursor-wait transition-colors"
          >
            ✕
          </button>
        </li>
      ))}
    </ul>
  );
}
