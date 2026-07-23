@echo off
REM Run all tests for SIGAP backend.
REM Usage: scripts\test.bat

cd /d "%~dp0.."

if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

set PYTHONPATH=backend

echo Running pytest...
pytest backend\app\tests\ -v --tb=short
