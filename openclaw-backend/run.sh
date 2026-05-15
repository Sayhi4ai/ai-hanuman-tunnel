#!/usr/bin/env bash
cd /home/inteligent-human/ai-bots/openclaw-backend
source /home/inteligent-human/ai-bots/openclaw-backend/venv/bin/activate
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8081
