import os
from typing import Dict, TypedDict, Any, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler
import logging

# Configuración de Observabilidad con Langfuse
langfuse_handler = CallbackHandler(
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY", "sk-lf-..."),
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY", "pk-lf-..."),
    host=os.environ.get("LANGFUSE_HOST", "http://localhost:3000")
)

# Estado del Grafo
class AgentState(TypedDict):
    messages: list[AnyMessage]
    current_intent: str
    selected_skill: str
    execution_result: str
    error_count: int

# Instanciar DeepSeek V3 como LLM Base
llm = ChatOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    temperature=0.2
)

def planner_node(state: AgentState):
    """Nodo Planner: Recibe instrucción del CEO y define la intención"""
    logging.info("[Planner] Analizando directiva del CEO...")
    messages = state.get("messages", [])
    
    # Prompt de planeación
    system_msg = SystemMessage(content="Eres el Planner de JARVIS. Tu objetivo es analizar el requerimiento del CEO y decidir qué acción tomar. Retorna SOLO una palabra clave de intención: [DEPLOY, BUILD, ANALYZE, REVENUE_CHECK, CHAT]")
    response = llm.invoke([system_msg] + messages, config={"callbacks": [langfuse_handler]})
    
    return {"current_intent": response.content.strip().upper(), "error_count": state.get("error_count", 0)}

def router_node(state: AgentState):
    """Nodo Router: Decide qué Skill ejecutar según la intención"""
    intent = state.get("current_intent", "")
    logging.info(f"[Router] Enrutando intención: {intent}")
    
    skill_map = {
        "DEPLOY": "sk_08", # Cloud Deploy
        "BUILD": "sk_06",  # Backend Forge
        "ANALYZE": "sk_02", # Market Analysis
        "REVENUE_CHECK": "sk_11" # Billing Automation
    }
    
    selected = skill_map.get(intent, "sk_10") # Default: Memory Sync
    return {"selected_skill": selected}

def executor_node(state: AgentState):
    """Nodo Executor: Ejecuta la Skill (Simulación con llamadas a herramientas MCP)"""
    skill = state.get("selected_skill")
    logging.info(f"[Executor] Ejecutando Skill: {skill}")
    
    try:
        # Simulando la ejecución de la skill seleccionada
        if skill == "sk_06":
            result = "Código backend generado con éxito."
        elif skill == "sk_11":
            result = "Métricas de facturación procesadas."
        else:
            result = f"Skill {skill} ejecutada satisfactoriamente."
            
        return {"execution_result": result, "error_count": 0}
    except Exception as e:
        error_count = state.get("error_count", 0) + 1
        return {"execution_result": f"ERROR: {str(e)}", "error_count": error_count}

def memory_node(state: AgentState):
    """Nodo Memory: Guarda en Mem0 y pgvector"""
    result = state.get("execution_result", "")
    logging.info("[Memory] Sincronizando contexto con Qdrant y pgvector...")
    # Aquí iría la lógica de mem0.add(result, user_id="CEO")
    return state

def reporter_node(state: AgentState):
    """Nodo Reporter: Envía alerta a Telegram"""
    result = state.get("execution_result", "")
    logging.info(f"[Reporter] Notificando a Telegram: {result}")
    # Aquí iría el código de requests.post a Telegram API
    return state

def should_retry(state: AgentState):
    """Edge Condicional: Verifica si debe reintentar tras un fallo"""
    if "ERROR" in state.get("execution_result", ""):
        if state.get("error_count", 0) < 3:
            logging.warning("[Circuit Breaker] Error detectado. Reintentando...")
            return "executor"
        else:
            logging.error("[Circuit Breaker] Max retries alcanzado. Fallback activado.")
            return "reporter" # Reportar el error final
    return "memory"

# Construcción del Grafo
workflow = StateGraph(AgentState)

# Agregar Nodos
workflow.add_node("planner", planner_node)
workflow.add_node("router", router_node)
workflow.add_node("executor", executor_node)
workflow.add_node("memory", memory_node)
workflow.add_node("reporter", reporter_node)

# Definir Flujo de Ejecución (Edges)
workflow.set_entry_point("planner")
workflow.add_edge("planner", "router")
workflow.add_edge("router", "executor")

# Edge Condicional para Circuit Breaker
workflow.add_conditional_edges(
    "executor",
    should_retry,
    {
        "executor": "executor",
        "reporter": "reporter",
        "memory": "memory"
    }
)

workflow.add_edge("memory", "reporter")
workflow.add_edge("reporter", END)

# Compilar Grafo
jarvis_app = workflow.compile()

if __name__ == "__main__":
    # Prueba de ejecución local
    logging.basicConfig(level=logging.INFO)
    initial_state = {"messages": [HumanMessage(content="Despliega el nuevo módulo backend de veterinaria.")], "error_count": 0}
    for output in jarvis_app.stream(initial_state):
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value)
        print("\n---\n")
