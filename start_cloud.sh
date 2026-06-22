#!/bin/bash

echo "======================================"
echo " INICIANDO JARVIS AX (CLOUD MODE v2)"
echo "======================================"

# Iniciar Bot de Telegram
echo "[OK] Iniciando Bot de Telegram..."
PYTHONIOENCODING=utf-8 python telegram_bot.py > telegram.log 2>&1 &

# Iniciar Worker Autónomo (CANAL QWEN-JARVIS)
echo "[OK] Iniciando Worker Autónomo v2..."
PYTHONIOENCODING=utf-8 python autonomous_worker.py > worker.log 2>&1 &

# Iniciar Omni Core Server (debe ir al frente)
echo "[OK] Iniciando Node Omni Core..."
exec node axyntrax-omni-core/omni_server.js
# rebuild trigger 2026-06-18T08:45:04.4949486-05:00
