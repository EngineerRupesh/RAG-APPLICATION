// ============================================================================
// DOCUMENT PANEL (left sidebar)
// ----------------------------------------------------------------------------
// Composes the upload dropzone, the indexed-document list, and the
// always-visible safety disclaimer. All state/logic lives in the parent
// page; this component is just layout.
// ============================================================================

import UploadDropzone from "./UploadDropzone";
import DocumentList from "./DocumentList";

export default function DocumentPanel({ documents, onUpload, onDelete, uploadStatus }) {
  return (
    <section className="bg-surface border-r border-border p-5 overflow-y-auto flex flex-col">
      <h2 className="font-display text-[13px] uppercase tracking-wider text-teal-700 mb-3">
        Knowledge base
      </h2>

      <UploadDropzone
        onFileSelected={onUpload}
        statusText={uploadStatus.text}
        statusKind={uploadStatus.kind}
      />

      <h3 className="font-display text-[13px] uppercase tracking-wider text-teal-700 mt-6 mb-2.5">
        Indexed documents
      </h3>
      <DocumentList documents={documents} onDelete={onDelete} />

      <div className="mt-auto pt-4">
        <div className="text-[11.5px] leading-relaxed text-[#8a6416] bg-amber-bg border border-[#ecd8ab] rounded-xl p-3">
          <strong className="text-amber">Not medical advice.</strong> Answers are
          generated only from documents you upload here and may be incomplete
          or wrong. Always consult a licensed healthcare professional for
          decisions about your own care.
        </div>
      </div>
    </section>
  );
}
