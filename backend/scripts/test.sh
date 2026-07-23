#!/bin/bash
# Run all tests for SIGAP backend.
# Usage: ./backend/scripts/test.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$BACKEND_DIR")"

cd "$PROJECT_ROOT"

# Use .venv Python directly if exists
if [ -f ".venv/Scripts/python.exe" ]; then
    PYTHON=".venv/Scripts/python.exe"
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "No Python found"
    exit 1
fi

export PYTHONPATH=backend

echo "Running pytest..."
"$PYTHON" -m pytest backend/app/tests/ -v --tb=short