#!/usr/bin/env bash
set -e

# Go to repo root
cd "$(dirname "$0")/.."

# Activate ops-base venv
source ops-base/bin/activate

# Run FastAPI app on port 9000
uvicorn openclaw_guardian.app:app --host 0.0.0.0 --port 9000
