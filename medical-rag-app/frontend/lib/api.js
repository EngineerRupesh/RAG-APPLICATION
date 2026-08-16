// ============================================================================
// API CLIENT
// ----------------------------------------------------------------------------
// Every call to the FastAPI backend goes through this file. Components never
// call fetch() directly - they call these functions, so the backend URL and
// error handling only need to be defined once.
// ============================================================================

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function handleResponse(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

// --- Health -------------------------------------------------------------
export async function getHealth() {
  const res = await fetch(`${API_BASE}/health`, { cache: "no-store" });
  return handleResponse(res);
}

// --- Documents -----------------------------------------------------------
export async function listDocuments() {
  const res = await fetch(`${API_BASE}/api/documents`, { cache: "no-store" });
  return handleResponse(res);
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/api/documents`, { method: "POST", body: formData });
  return handleResponse(res);
}

export async function deleteDocument(docId) {
  const res = await fetch(`${API_BASE}/api/documents/${docId}`, { method: "DELETE" });
  return handleResponse(res);
}

// --- Chat (text only) ------------------------------------------------------
export async function sendChatMessage(question) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return handleResponse(res);
}

// --- Evaluation (RAGAS) -------------------------------------------------
export async function getRagasResults() {
  const res = await fetch(`${API_BASE}/api/evaluation/ragas`, { cache: "no-store" });
  return handleResponse(res);
}

export async function evaluateAnswer(question, answer, contexts, groundTruth = null) {
  const res = await fetch(`${API_BASE}/api/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      answer,
      contexts,
      ground_truth: groundTruth,
    }),
  });
  return handleResponse(res);
}
