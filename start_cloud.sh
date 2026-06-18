#!/bin/bash

echo "======================================"
echo " INICIANDO JARVIS AX (CLOUD MODE)"
echo "======================================"

# Iniciar Bot de Telegram
echo "[OK] Iniciando Bot de Telegram..."
python telegram_bot.py > telegram.log 2>&1 &

# Iniciar Worker Autónomo (EL CANAL QWEN-JARVIS)
echo "[OK] Iniciando Worker Autónomo v2..."
python autonomous_worker.py > worker.log 2>&1 &

# Iniciar FastAPI
echo "[OK] Iniciando FastAPI..."
exec python -m uvicorn backend.jarvis_orchestrator.main:app --host 0.0.0.0 --port 8080
