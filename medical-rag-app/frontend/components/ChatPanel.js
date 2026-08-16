// ============================================================================
// CHAT PANEL (right side)
// ----------------------------------------------------------------------------
// Scrollable message log plus the text-only input row. Auto-scrolls to the
// latest message whenever the conversation changes.
// ============================================================================

"use client";

import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import RagasPanel from "./RagasPanel";

export default function ChatPanel({ messages, onSend, sending, ragasResults }) {
  const logRef = useRef(null);

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight });
  }, [messages]);

  return (
    <section className="flex flex-col overflow-hidden">
      <div ref={logRef} className="flex-1 overflow-y-auto px-8 py-6 flex flex-col gap-4">
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} text={m.text} sources={m.sources} pending={m.pending} ragas={m.ragas} />
        ))}
      </div>

      {ragasResults && <div className="px-8"><RagasPanel results={ragasResults} /></div>}

      <ChatInput onSend={onSend} disabled={sending} />
    </section>
  );
}
