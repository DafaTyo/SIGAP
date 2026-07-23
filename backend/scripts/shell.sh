#!/bin/bash
# Open a Python REPL with SIGAP backend loaded.
# Usage: ./backend/scripts/shell.sh

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

echo "Starting Python shell with SIGAP loaded..."
"$PYTHON" -c "
import sys
sys.path.insert(0, 'backend')
from app.core.config import settings
from app.domains.vendor.models import Vendor
from app.domains.distribution.models import DistributionReport
from app.domains.complaint.models import Complaint

print('=== SIGAP Shell Ready ===')
print(f'ENV: {settings.ENV}')
print(f'DB: {settings.DATABASE_URL}')
print('Available models: Vendor, DistributionReport, Complaint')
"