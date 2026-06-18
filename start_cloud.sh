#!/bin/bash

echo "======================================"
echo " INICIANDO JARVIS AX (CLOUD MODE)"
echo "======================================"

# Iniciar Puente Qwen-JARVIS
echo "[OK] Iniciando Puente Qwen-JARVIS..."
python backend/jarvis_orchestrator/qwen_bridge.py > qwen_bridge.log 2>&1 &

# Iniciar CHAU CHAMBA
echo "[OK] Iniciando CHAU CHAMBA (Bot 24/7)..."
python chau_chamba.py > chau_chamba.log 2>&1 &

# Iniciar FastAPI
echo "[OK] Iniciando Orquestador (FastAPI)..."
python -m uvicorn backend.jarvis_orchestrator.main:app --host 0.0.0.0 --port 8080