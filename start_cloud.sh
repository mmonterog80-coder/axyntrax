#!/bin/bash

# Iniciar Qwen Bridge Worker en background
echo "Iniciando Puente Qwen-JARVIS..."
nohup python backend/jarvis_orchestrator/qwen_bridge.py > qwen_bridge.log 2>&1 &

# Iniciar CHAU CHAMBA en background
echo "Iniciando CHAU CHAMBA..."
nohup python chau_chamba.py > chau_chamba.log 2>&1 &

# Iniciar FastAPI
echo "Iniciando API..."
python -m uvicorn backend.jarvis_orchestrator.main:app --host 0.0.0.0 --port 8080
