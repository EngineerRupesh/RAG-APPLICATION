// ============================================================================
// CHAT INPUT
// ----------------------------------------------------------------------------
// The ONLY way the user talks to the assistant: a plain text field + send
// button. No microphone, no voice input anywhere in this component or app.
// ============================================================================

"use client";

import { useState } from "react";

export default function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const question = value.trim();
    if (!question) return;
    onSend(question);
    setValue("");
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2.5 px-8 py-4.5 border-t border-border bg-surface shrink-0">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Ask a question about your uploaded documents…"
        autoComplete="off"
        required
        className="flex-1 px-4 py-3 border border-border rounded-xl text-[14.5px] bg-bg text-ink outline-none focus:border-teal-500 focus:bg-surface transition-colors"
      />
      <button
        type="submit"
        disabled={disabled}
        className="px-5 rounded-xl bg-teal-700 text-white font-display font-semibold text-sm hover:bg-teal-900 disabled:bg-[#a9beba] disabled:cursor-wait transition-colors"
      >
        Send
      </button>
    </form>
  );
}
