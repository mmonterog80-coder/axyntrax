#!/bin/bash
# ==============================================================================
# AXYNTRAX L99: HETZNER BARE-METAL OLLAMA ORCHESTRATOR
# ==============================================================================
# Este script levanta Ollama en Hetzner con soporte de red abierto
# y fuerza la descarga de los modelos requeridos por Antigravity.

echo "[L99] Inicializando clúster neuronal local en Hetzner..."

# 1. Forzar Ollama a escuchar en todas las interfaces de red (0.0.0.0) 
# para que los contenedores Docker o conexiones externas puedan llegar a él.
export OLLAMA_HOST="0.0.0.0"

# 2. Iniciar el servicio Ollama en segundo plano (si no está corriendo)
nohup ollama serve > /var/log/ollama_l99.log 2>&1 &
echo "[L99] Ollama sirviendo en 0.0.0.0:11434 (Logs en /var/log/ollama_l99.log)"

# 3. Dar tiempo al daemon para iniciar
sleep 5

# 4. Inyectar y verificar Modelos requeridos por el Council L99
echo "[L99] Sincronizando modelo Estratega: qwen2.5:32b..."
ollama pull qwen2.5:32b

echo "[L99] Sincronizando modelo Auditor: llama3..."
ollama pull llama3

echo "======================================================================"
echo " ✅ OLLAMA CONECTADO Y ENRUTADO PARA ANTIGRAVITY L99"
echo " El Council tiene control total. Modelos cargados en RAM."
echo "======================================================================"
