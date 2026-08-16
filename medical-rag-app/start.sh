#!/usr/bin/env bash
# ============================================================================
# SETUP + RUN SCRIPT (Linux / macOS)
# ----------------------------------------------------------------------------
# Sets up and starts BOTH halves of the app:
#   - backend  (FastAPI, port 8000)  - the RAG API
#   - frontend (Next.js, port 3000)  - the UI
#
# Usage:
#   chmod +x start.sh
#   ./start.sh
# ============================================================================
set -e
cd "$(dirname "$0")"

# --- Backend: venv + deps + .env --------------------------------------------
echo "== Backend =="
cd backend
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi
source venv/bin/activate

echo "Installing backend dependencies (first run downloads ~2GB of ML libraries, be patient)..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

if [ ! -f ".env" ]; then
  echo "Creating backend/.env from template..."
  cp ../.env.example .env
  echo ""
  echo "!!! IMPORTANT: open backend/.env and set GEMINI_API_KEY before continuing !!!"
  echo "Get a free key at: https://aistudio.google.com/apikey"
  echo ""
  read -p "Press Enter once you've added your GEMINI_API_KEY to backend/.env..."
fi

echo "Starting backend at http://localhost:8000 ..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Make sure the backend is always stopped when this script exits.
trap "echo Stopping backend...; kill $BACKEND_PID 2>/dev/null" EXIT

# --- Frontend: npm install + .env.local -------------------------------------
echo ""
echo "== Frontend =="
cd frontend
if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi
if [ ! -f ".env.local" ]; then
  cp .env.local.example .env.local
fi

echo "Starting frontend at http://localhost:3000 ..."
npm run dev
