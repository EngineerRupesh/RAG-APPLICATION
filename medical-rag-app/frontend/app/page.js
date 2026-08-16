// ============================================================================
// MAIN PAGE
// ----------------------------------------------------------------------------
// The whole app is one screen: a document panel on the left, a chat panel
// on the right. This component owns all shared state (health, documents,
// chat history) and passes data + handlers down to the presentational
// components in components/.
// ============================================================================

"use client";

import { useEffect, useState, useCallback } from "react";
import Header from "../components/Header";
import DocumentPanel from "../components/DocumentPanel";
import ChatPanel from "../components/ChatPanel";
import RagasPanel from "../components/RagasPanel";
import { getHealth, listDocuments, uploadDocument, deleteDocument, sendChatMessage, getRagasResults } from "../lib/api";

const WELCOME_MESSAGE = {
  role: "assistant",
  text:
    "Hi — upload one or more medical PDFs on the left, then ask me questions " +
    "about them in the box below. I only answer using what's in your documents.",
};

export default function Page() {
  const [health, setHealth] = useState(null); // null = loading, "down" = unreachable, else object
  const [documents, setDocuments] = useState([]);
  const [uploadStatus, setUploadStatus] = useState({ text: "", kind: "" });
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [sending, setSending] = useState(false);
  const [ragasResults, setRagasResults] = useState(null);

  // --- SECTION 1: health polling ------------------------------------------
  const refreshHealth = useCallback(async () => {
    try {
      setHealth(await getHealth());
    } catch {
      setHealth("down");
    }
  }, []);

  useEffect(() => {
    refreshHealth();
    const interval = setInterval(refreshHealth, 8000);
    return () => clearInterval(interval);
  }, [refreshHealth]);

  // --- SECTION 2: document list -------------------------------------------
  const refreshDocuments = useCallback(async () => {
    try {
      setDocuments(await listDocuments());
    } catch {
      // Leave the previous list in place if this poll fails.
    }
  }, []);

  useEffect(() => {
    refreshDocuments();
  }, [refreshDocuments]);

  // --- SECTION 2B: RAGAS results ------------------------------------------
  const refreshRagasResults = useCallback(async () => {
    try {
      setRagasResults(await getRagasResults());
    } catch {
      // Leave the previous results in place if this poll fails.
    }
  }, []);

  useEffect(() => {
    refreshRagasResults();
    const interval = setInterval(refreshRagasResults, 30000); // Poll every 30 seconds
    return () => clearInterval(interval);
  }, [refreshRagasResults]);

  // --- SECTION 3: upload ---------------------------------------------------
  async function handleUpload(file) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setUploadStatus({ text: "Only PDF files are supported.", kind: "error" });
      return;
    }
    setUploadStatus({ text: `Indexing "${file.name}"… this can take a moment.`, kind: "" });

    try {
      await uploadDocument(file);
      setUploadStatus({ text: `"${file.name}" indexed successfully.`, kind: "success" });
      await Promise.all([refreshDocuments(), refreshHealth()]);
    } catch (err) {
      setUploadStatus({ text: err.message, kind: "error" });
    }
  }

  // --- SECTION 4: delete -----------------------------------------------------
  async function handleDelete(docId) {
    await deleteDocument(docId);
    await Promise.all([refreshDocuments(), refreshHealth()]);
  }

  // --- SECTION 5: chat (text only - no voice input in this app) ------------
  async function handleSend(question) {
    setMessages((prev) => [...prev, { role: "user", text: question }, { role: "assistant", text: "Thinking…", pending: true }]);
    setSending(true);

    try {
      const data = await sendChatMessage(question);
      setMessages((prev) => {
        const next = [...prev];
        next[next.length - 1] = { role: "assistant", text: data.answer, sources: data.sources, ragas: data.ragas };
        return next;
      });
    } catch (err) {
      setMessages((prev) => {
        const next = [...prev];
        next[next.length - 1] = { role: "assistant", text: `⚠️ ${err.message}` };
        return next;
      });
    } finally {
      setSending(false);
    }
  }

  return (
    <>
      <Header health={health} />
      <main className="flex-1 grid grid-cols-[320px_1fr] max-md:grid-cols-1 max-md:grid-rows-[auto_1fr] overflow-hidden">
        <DocumentPanel
          documents={documents}
          onUpload={handleUpload}
          onDelete={handleDelete}
          uploadStatus={uploadStatus}
        />
        <ChatPanel messages={messages} onSend={handleSend} sending={sending} ragasResults={ragasResults} />
      </main>
    </>
  );
}
