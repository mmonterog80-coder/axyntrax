import asyncio
import sys
import os

# Añadir el orquestador al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'jarvis_orchestrator'))

from scheduler import autonomous_decision_cycle

async def test_proactive():
    print("[TEST] Forzando el despertar del Módulo Proactivo de JARVIS...")
    await autonomous_decision_cycle()
    print("[TEST] JARVIS ha terminado de pensar.")

if __name__ == "__main__":
    asyncio.run(test_proactive())
