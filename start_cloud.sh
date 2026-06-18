#!/bin/bash

echo 'Iniciando JARVIS AX Autónomo...'

python telegram_bot.py > telegram.log 2>&1 &
python autonomous_worker.py > worker.log 2>&1 &
python backend/jarvis_orchestrator/qwen_bridge.py > bridge.log 2>&1 &

python -m uvicorn backend.jarvis_orchestrator.main:app --host 0.0.0.0 --port 8080
