import os
import logging
from typing import Dict, TypedDict, Any, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler
import httpx
import asyncio
import json

# Configuración de Observabilidad con Langfuse
langfuse_handler = CallbackHandler(
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY", "sk-lf-..."),
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY", "pk-lf-..."),
    host=os.environ.get("LANGFUSE_HOST", "http://localhost:3000")
)

# LLM Base
llm = ChatOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    temperature=0.2
)

# ==========================================
# 1. ESTADO DEL GRAFO (AXYNTRAXState)
# ==========================================
class AXYNTRAXState(TypedDict):
    current_skill: str          # "SKILL_01" | "SKILL_02" | ...
    retry_count: int            # 0-3 max
    error_log: List[str]        # Errores detectados
    checkpoints: Dict[str, Any] # Estado de cada skill completada
    directive: str              # Orden original de Miguel
    output: Dict[str, Any]      # Resultado acumulado
    next_skill: str             # Skill siguiente a ejecutar
    valid: bool                 # Flag de validación

# ==========================================
# 2. NODOS DEL GRAFO
# ==========================================

async def directive_planner(state: AXYNTRAXState):
    """SKILL 11: Directive Validation & Ack (Sentinel)"""
    logging.info("[Planner] Sentinel validando directiva...")
    directive = state.get("directive", "")
    
    # Simulación de validación (idealmente llamaría al MCP /validate_directive)
    valid = len(directive) > 10
    if not valid:
        return {
            "error_log": state.get("error_log", []) + ["Directiva ambigua o muy corta"],
            "output": {"suggestion": "Proporcione más detalles de la tarea."},
            "valid": False
        }
    return {"current_skill": "SKILL_01", "next_skill": "SKILL_02", "valid": True}

async def skill_router(state: AXYNTRAXState):
    """Decide qué skill ejecutar"""
    skill = state.get("current_skill", "SKILL_01")
    logging.info(f"[Router] Enrutando a {skill}")
    return {"current_skill": skill}

async def skill_executor(state: AXYNTRAXState):
    """Ejecuta la Skill asignada"""
    skill = state.get("current_skill")
    logging.info(f"[Executor] Ejecutando {skill}")
    
    try:
        # Simulando ejecución
        result = f"Resultado exitoso de {skill}"
        checkpoints = state.get("checkpoints", {})
        checkpoints[skill] = result
        
        output = state.get("output", {})
        output[skill] = result
        
        return {
            "checkpoints": checkpoints,
            "output": output
        }
    except Exception as e:
        error_log = state.get("error_log", [])
        error_log.append(str(e))
        return {
            "error_log": error_log,
            "retry_count": state.get("retry_count", 0) + 1,
            "valid": False
        }

async def acceptance_validator(state: AXYNTRAXState):
    """SKILL 14: Acceptance Criteria Validator"""
    skill = state.get("current_skill")
    logging.info(f"[Validator] Validando output de {skill}")
    
    # Simulando validación
    output = state.get("output", {}).get(skill, "")
    passed = "exit" in output.lower() or "exitoso" in output.lower()
    
    if not passed:
        error_log = state.get("error_log", [])
        error_log.append(f"Criterios faltantes en {skill}")
        return {
            "valid": False,
            "error_log": error_log
        }
    
    return {"valid": True, "current_skill": state.get("next_skill", "FINISH")}

async def retry_handler(state: AXYNTRAXState):
    """SKILL 12: Retry Loop con Circuit Breaker"""
    retry_count = state.get("retry_count", 0)
    logging.warning(f"[Retry Handler] Iniciando retry {retry_count + 1}/3 con circuit breaker")
    
    # Exponential backoff simulado
    await asyncio.sleep(1)
    
    return {"retry_count": retry_count + 1}

async def progress_reporter(state: AXYNTRAXState):
    """SKILL 13: StateManager & Progress Report"""
    logging.info("[Reporter] Enviando progreso a Telegram...")
    
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if bot_token and chat_id:
        msg = f"🚀 *AXYNTRAX Progress Report*\n"
        msg += f"📍 Skill: {state.get('current_skill', 'N/A')}\n"
        msg += f"⏱️ Retries: {state.get('retry_count', 0)}/3\n"
        msg += f"❌ Errores: {len(state.get('error_log', []))}\n"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        try:
            async with httpx.AsyncClient() as client:
                await client.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
        except Exception as e:
            logging.error(f"Fallo al reportar a telegram: {e}")
            
    return state

# ==========================================
# 3. CONSTRUCCIÓN DEL GRAFO
# ==========================================

builder = StateGraph(AXYNTRAXState)

# Registrar Nodos
builder.add_node("planner", directive_planner)
builder.add_node("router", skill_router)
builder.add_node("executor", skill_executor)
builder.add_node("validator", acceptance_validator)
builder.add_node("reporter", progress_reporter)
builder.add_node("retry", retry_handler)

# Configurar Flujo (Edges)
builder.set_entry_point("planner")

# Del planner puede ir a reporte si falla la directiva, si no a router
def planner_condition(state: AXYNTRAXState):
    if not state.get("valid", True):
        return "reporter"
    return "router"

builder.add_conditional_edges("planner", planner_condition, {"reporter": "reporter", "router": "router"})
builder.add_edge("router", "executor")
builder.add_edge("executor", "validator")

# Lógica del Circuit Breaker (Validar si continúa o hace retry)
def validator_condition(state: AXYNTRAXState):
    if not state.get("valid", True) and state.get("retry_count", 0) < 3:
        return "retry"
    return "reporter"

builder.add_conditional_edges("validator", validator_condition, {"retry": "retry", "reporter": "reporter"})
builder.add_edge("retry", "executor")
builder.add_edge("reporter", END)

# Compilar
jarvis_app = builder.compile()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Ejecución de prueba
    async def run_test():
        initial_state = {
            "directive": "Construye el módulo de veterinaria completo",
            "current_skill": "SKILL_01",
            "retry_count": 0,
            "error_log": [],
            "checkpoints": {},
            "output": {},
            "valid": True
        }
        
        async for output in jarvis_app.astream(initial_state):
            for key, value in output.items():
                print(f"\n[{key.upper()}] >>> {value}")
                
    asyncio.run(run_test())
