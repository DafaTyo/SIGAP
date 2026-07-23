@echo off
REM Run the SIGAP FastAPI server locally.
REM Usage: scripts\run.bat

cd /d "%~dp0.."

if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

set PYTHONPATH=backend

echo Starting SIGAP API server...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
