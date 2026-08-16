@echo off
REM ============================================================================
REM SETUP + RUN SCRIPT (Windows)
REM ----------------------------------------------------------------------------
REM Sets up and starts BOTH halves of the app:
REM   - backend  (FastAPI, port 8000)  - the RAG API   (new console window)
REM   - frontend (Next.js, port 3000)  - the UI          (this window)
REM
REM Usage: double-click start.bat, or run it from a terminal.
REM ============================================================================

cd /d "%~dp0backend"

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

echo Installing backend dependencies (first run downloads ~2GB of ML libraries, be patient)...
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

if not exist .env (
    echo Creating backend\.env from template...
    copy ..\.env.example .env
    echo.
    echo !!! IMPORTANT: open backend\.env and set GEMINI_API_KEY before continuing !!!
    echo Get a free key at: https://aistudio.google.com/apikey
    echo.
    pause
)

echo Starting backend at http://localhost:8000 in a new window...
start "MedGrounded Backend" cmd /k "call venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000"

cd /d "%~dp0frontend"
if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
)
if not exist .env.local (
    copy .env.local.example .env.local
)

echo Starting frontend at http://localhost:3000 ...
call npm run dev
