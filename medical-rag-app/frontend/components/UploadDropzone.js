// ============================================================================
// UPLOAD DROPZONE
// ----------------------------------------------------------------------------
// Click-to-browse + drag-and-drop area for PDF uploads. Purely presentational
// plus drag-state handling - the actual upload call lives in the parent page.
// ============================================================================

"use client";

import { useRef, useState } from "react";

export default function UploadDropzone({ onFileSelected, statusText, statusKind }) {
  const inputRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);

  function handleDrop(e) {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) onFileSelected(file);
  }

  const statusColor =
    statusKind === "error" ? "text-red-700" : statusKind === "success" ? "text-teal-700" : "text-ink-soft";

  return (
    <div>
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        className={`w-full text-center border-[1.5px] border-dashed rounded-2xl px-3.5 py-5 transition-colors ${
          isDragOver ? "bg-[#d6ece8] border-teal-700" : "bg-teal-100 border-teal-500 hover:bg-[#d6ece8]"
        }`}
      >
        <div className="text-2xl font-semibold text-teal-700">＋</div>
        <p className="mt-1.5 text-sm text-ink-soft leading-snug">
          <strong className="text-teal-900">Upload a medical PDF</strong>
          <br />
          click to browse or drop a file
        </p>
      </button>

      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        hidden
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onFileSelected(file);
          e.target.value = ""; // allow re-selecting the same file later
        }}
      />

      <div className={`font-mono text-xs min-h-[18px] mt-2 px-0.5 ${statusColor}`}>{statusText}</div>
    </div>
  );
}
