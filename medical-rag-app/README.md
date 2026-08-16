# Medical Assistant RAG Application

A production-shaped Retrieval-Augmented-Generation application that answers
medical questions **only** using PDFs you upload. Text-only input (no
voice), a health check endpoint, document delete, a Next.js UI, and a
RAGAS evaluation script are all included.

```
PDF upload → chunking → local embeddings → FAISS index → rerank
           → LCEL prompt/LLM step → answer generation
```

## Project layout

Every operation gets its own small, single-responsibility file:

```
medical-rag-app/
├── backend/                            # FastAPI JSON API (Python)
│   ├── main.py                          # App wiring only: CORS + routers
│   ├── config.py                        # All settings, loaded from .env
│   ├── schemas.py                       # Pydantic request/response models
│   │
│   ├── routes/                          # HTTP layer - one router per topic
│   │   ├── health_routes.py              # GET /health
│   │   ├── document_routes.py            # POST/GET/DELETE /api/documents
│   │   └── chat_routes.py                # POST /api/chat (text-only Q&A)
│   │
│   ├── services/                        # Business logic - one file per operation
│   │   ├── embedding_service.py          # Loads the local embedding model
│   │   ├── chunking_service.py           # PDF loading + text splitting
│   │   ├── vector_store_service.py       # All FAISS ops: add/delete/search/save
│   │   ├── reranker_service.py           # Cross-encoder reranking of candidates
│   │   ├── llm_service.py                # Chat-model factory (Gemini/OpenAI/Anthropic/Ollama)
│   │   ├── rag_service.py                # LCEL chain: orchestrates the above
│   │   └── document_service.py           # Ingestion + doc registry (metadata.json)
│   │
│   ├── requirements.txt
│   ├── uploads/                          # Uploaded PDFs (created at runtime)
│   └── vectorstore/                      # FAISS index + metadata.json (created at runtime)
│
├── frontend/                           # Next.js UI (App Router, JavaScript)
│   ├── app/
│   │   ├── layout.js                     # Fonts + global HTML shell
│   │   ├── page.js                       # Owns app state, wires panels together
│   │   └── globals.css                   # Tailwind + a couple of custom rules
│   ├── components/
│   │   ├── Header.js                     # Brand mark + ECG signature
│   │   ├── HealthIndicator.js            # Live backend status dot
│   │   ├── DocumentPanel.js              # Left sidebar layout
│   │   ├── UploadDropzone.js             # Click / drag & drop PDF upload
│   │   ├── DocumentList.js               # Indexed docs + delete buttons
│   │   ├── ChatPanel.js                  # Scrollable message log + input
│   │   ├── ChatMessage.js                # One bubble + source citations
│   │   └── ChatInput.js                  # Text field only - no voice input
│   ├── lib/api.js                        # Every backend fetch call, in one place
│   ├── package.json
│   ├── tailwind.config.js                # Teal clinical color palette
│   └── .env.local.example
│
├── evaluation/
│   └── ragas_evaluation.py              # RAGAS quality assessment script
├── start.sh / start.bat                 # One-command setup + run (both servers)
├── .env.example                         # Backend environment template
└── README.md
```

Each backend service does exactly one job and only talks to the layer
below it: `routes` call `services`, `rag_service` calls
`vector_store_service` + `reranker_service` + `llm_service`, and nothing
reaches into FAISS, the reranker model, or the LLM client except through
its dedicated service file. On the frontend, every component is
presentational; all shared state and every backend call live in
`app/page.js` and `lib/api.js` respectively.



The script sets up a Python virtual environment, installs backend
dependencies, installs frontend `npm` packages, and on first run pauses so
you can paste your **free Gemini API key** into `backend/.env` (get one at
https://aistudio.google.com/apikey). After that it starts both servers
automatically — every future run just launches straight away.

Open **http://localhost:3000** for the app UI once it's running. The API
itself runs at **http://localhost:8000**.

## 1. Manual setup (if you prefer doing it by hand)

**Backend:**
```bash
cd medical-rag-app/backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp ../.env.example .env         # then edit .env and set GEMINI_API_KEY

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend** (in a second terminal):
```bash
cd medical-rag-app/frontend
npm install
cp .env.local.example .env.local   # default already points at localhost:8000
npm run dev
```

RAGAS RUN SCTRIPT
python evaluation/ragas_evaluation.py

Open **http://localhost:3000**.

By default the app uses **Google Gemini** (`LLM_PROVIDER=gemini` in
`backend/.env`) — get a free key at https://aistudio.google.com/apikey.
OpenAI and Anthropic are also supported; just change `LLM_PROVIDER` in
`.env` and set the matching key. A fully **local Llama model via Ollama**
is also supported — no API key or internet call needed at inference time:

```bash
# 1) install Ollama: https://ollama.com
# 2) pull a model once
ollama pull llama3.1
# 3) in backend/.env:
LLM_PROVIDER=ollama
OLLAMA_MODEL_NAME=llama3.1
```

Embeddings run locally via `sentence-transformers` — no key required for
that part; the model weights download once from HuggingFace on first run.

## 2. Using the app

- Upload a PDF from the sidebar (click or drag & drop).
- Ask questions in the text field at the bottom of the chat panel.
- Click the ✕ next to a document to delete it (removes its vectors from
  the FAISS index immediately).
- The header status dot polls `GET /health` every few seconds so you
  always know whether the backend + index are reachable.

## 3. API reference

| Method | Path                  | Description                              |
|--------|-----------------------|-------------------------------------------|
| GET    | `/health`              | Health check                              |
| POST   | `/api/documents`       | Upload a PDF (multipart `file`)           |
| GET    | `/api/documents`       | List indexed documents                    |
| DELETE | `/api/documents/{id}`  | Delete a document + its vectors           |
| POST   | `/api/chat`            | `{ "question": "..." }` → grounded answer |

Interactive docs: **http://localhost:8000/docs**

## 4. Evaluate quality with RAGAS

1. Upload the PDF(s) you want to evaluate against.
2. Edit `evaluation/ragas_evaluation.py` → `EVAL_SET` with real
   question/ground-truth pairs for your documents.
3. Run:
   ```bash
   cd backend/evaluation
   python ragas_evaluation.py
   ```
4. Scores (`faithfulness`, `answer_relevancy`, `context_precision`,
   `context_recall`) print to the console and are saved to
   `ragas_results.csv`.

## 5. Design notes

- **Local embeddings** (`embedding_service.py`): `sentence-transformers/all-MiniLM-L6-v2`
  — fast, small, and runs on CPU with no external API call.
- **FAISS** (`vector_store_service.py`): persisted to `backend/vectorstore/`
  so the index survives restarts. Deleting a document calls
  `FAISS.delete(ids)` against the exact chunk ids recorded at ingestion
  time, then re-saves the index.
- **Reranking** (`reranker_service.py`): FAISS first returns a wide
  candidate set (`RETRIEVE_K`, default 10), then a local cross-encoder
  (`cross-encoder/ms-marco-MiniLM-L-6-v2`) re-scores question+chunk pairs
  together and keeps only the best `RERANK_TOP_K` (default 4) for
  generation — meaningfully more accurate than vector similarity alone.
- **LLM call** (`llm_service.py`): one factory function, provider chosen
  via `LLM_PROVIDER` in `.env` (`gemini` by default, or `openai`/`anthropic`/`ollama`).
  `ollama` runs a local Llama model with no API key and no internet call
  at inference time — see the Ollama section above.
- **LCEL chain** (`rag_service.py`): built with `RunnableParallel`/`itemgetter`
  so retrieval + reranking happens once and both the generated answer and
  its source chunks come back from a single `chain.invoke(...)` call.
- **Frontend** (`frontend/`): Next.js App Router, plain JavaScript, Tailwind
  for styling. `lib/api.js` is the only file that talks to the backend;
  `app/page.js` owns state and every other component is presentational.
- **Safety**: the system prompt restricts the LLM to the retrieved
  context only, and the UI always shows a "not medical advice" notice.


