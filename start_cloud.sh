#!/bin/bash

echo "======================================"
echo " INICIANDO JARVIS AX (CLOUD MODE) "
echo "======================================"

# El puerto es inyectado por Railway/Render
export PORT=${PORT:-8000}

# Si existe RAILWAY_PUBLIC_DOMAIN, configurar el webhook de Telegram o registrar la URL pública
if [ ! -z "$RAILWAY_PUBLIC_DOMAIN" ]; then
    echo "URL pública detectada: https://$RAILWAY_PUBLIC_DOMAIN"
    export ORCHESTRATOR_URL="https://$RAILWAY_PUBLIC_DOMAIN"
fi

# 1. Iniciar CHAU CHAMBA en segundo plano
echo "[OK] Iniciando CHAU CHAMBA (Bot 24/7) en segundo plano..."
python /app/chau_chamba.py &

# 2. Iniciar Orquestador en el primer plano
echo "[OK] Iniciando Orquestador (FastAPI)..."
cd /app/backend/jarvis_orchestrator
uvicorn main:app --host 0.0.0.0 --port $PORT
