import os
import sqlite3
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# ----------------------------------------------------
# 1. DURABLE CHECKPOINTER CONFIG
# ----------------------------------------------------
# We use SqliteSaver connected to a local SQLite file for durable, production persistence.
DB_PATH = "C:\\AXYNTRAX\\backend\\jarvis_orchestrator\\checkpoints.sqlite"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
checkpointer = SqliteSaver(conn)

# ----------------------------------------------------
# 2. STATE MODEL (TypedDict for LangGraph)
# ----------------------------------------------------
class AXYNTRAXState(TypedDict):
    directive: str
    current_skill: Optional[str]
    current_step: str
    retry_count: int
    max_retries: int
    error_log: List[str]
    checkpoints: Dict[str, Any]
    output: str
    next_skill: Optional[str]
    status: str
    thread_id: str

# ----------------------------------------------------
# 3. NODE RESPONSIBILITIES
# ----------------------------------------------------

def planner(state: AXYNTRAXState):
    print(f"[PLANNER] Thread: {state['thread_id']} | Normalizing directive: {state['directive']}")
    return {"current_step": "planner", "status": "planning_complete"}

def router(state: AXYNTRAXState):
    print(f"[ROUTER] Thread: {state['thread_id']} | Deciding next skill...")
    # Simulated routing logic
    next_s = "skill_1" if not state.get("current_skill") else "skill_2"
    return {"current_skill": next_s, "current_step": "router", "status": "routed"}

def executor(state: AXYNTRAXState):
    print(f"[EXECUTOR] Thread: {state['thread_id']} | Executing skill: {state['current_skill']}")
    
    # Simulating a failure on the first attempt of skill_1 to test retry logic
    if state["current_skill"] == "skill_1" and state["retry_count"] == 0:
        return {
            "current_step": "executor",
            "status": "error",
            "output": "Simulated exception during MCP tool execution."
        }
        
    return {
        "current_step": "executor",
        "status": "success",
        "output": f"Executed {state['current_skill']} successfully."
    }

def validator(state: AXYNTRAXState):
    print(f"[VALIDATOR] Thread: {state['thread_id']} | Validating output: {state['status']}")
    if state["status"] == "error":
        return {"current_step": "validator", "status": "needs_retry"}
    
    # If successful and it was skill_1, route back for skill_2
    if state["current_skill"] == "skill_1":
        return {"current_step": "validator", "status": "continue_routing"}
        
    return {"current_step": "validator", "status": "completed"}

def retry_handler(state: AXYNTRAXState):
    new_retry = state["retry_count"] + 1
    print(f"[RETRY_HANDLER] Thread: {state['thread_id']} | Attempt {new_retry} of {state['max_retries']}")
    
    if new_retry >= state["max_retries"]:
        return {
            "retry_count": new_retry,
            "current_step": "retry_handler",
            "status": "fatal_error",
            "error_log": state["error_log"] + [f"Max retries exceeded at {state['current_skill']}"]
        }
    
    return {
        "retry_count": new_retry,
        "current_step": "retry_handler",
        "status": "retry_approved"
    }

def failure_handler(state: AXYNTRAXState):
    print(f"[FAILURE_HANDLER] Thread: {state['thread_id']} | Capturing unrecoverable failure!")
    return {"current_step": "failure_handler", "status": "aborted"}

def reporter(state: AXYNTRAXState):
    print(f"[REPORTER] Thread: {state['thread_id']} | Sending telemetry. Final Status: {state['status']}")
    return {"current_step": "reporter", "checkpoints": {state['current_step']: "reported"}}

# ----------------------------------------------------
# 4. CONDITIONAL EDGES
# ----------------------------------------------------

def route_after_validator(state: AXYNTRAXState) -> str:
    if state["status"] == "needs_retry":
        return "retry_handler"
    elif state["status"] == "continue_routing":
        return "router"
    else:
        return "reporter"

def route_after_retry(state: AXYNTRAXState) -> str:
    if state["status"] == "fatal_error":
        return "failure_handler"
    return "executor"

# ----------------------------------------------------
# 5. BUILD GRAPH
# ----------------------------------------------------
builder = StateGraph(AXYNTRAXState)

builder.add_node("planner", planner)
builder.add_node("router", router)
builder.add_node("executor", executor)
builder.add_node("validator", validator)
builder.add_node("retry_handler", retry_handler)
builder.add_node("reporter", reporter)
builder.add_node("failure_handler", failure_handler)

builder.set_entry_point("planner")
builder.add_edge("planner", "router")
builder.add_edge("router", "executor")
builder.add_edge("executor", "validator")

builder.add_conditional_edges(
    "validator",
    route_after_validator,
    {
        "retry_handler": "retry_handler",
        "router": "router",
        "reporter": "reporter"
    }
)

builder.add_conditional_edges(
    "retry_handler",
    route_after_retry,
    {
        "executor": "executor",
        "failure_handler": "failure_handler"
    }
)

builder.add_edge("failure_handler", "reporter")
builder.add_edge("reporter", END)

# Compile with durable checkpointer
app = builder.compile(checkpointer=checkpointer)

# ----------------------------------------------------
# 6. INVOCATION EXAMPLE & TEST
# ----------------------------------------------------
def run_antigravity_flow(directive: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    
    # We must properly initialize the State since we are using TypedDict and operator updates
    # Actually, in standard LangGraph, if a key is not provided it may fail. Let's provide all defaults.
    initial_state = {
        "directive": directive,
        "current_skill": None,
        "current_step": "init",
        "retry_count": 0,
        "max_retries": 3,
        "error_log": [],
        "checkpoints": {},
        "output": "",
        "next_skill": None,
        "status": "initialized",
        "thread_id": thread_id
    }
    
    print("\n" + "="*50)
    print(f" INICIANDO RUN DURABLE | Thread: {thread_id}")
    print("="*50)
    
    for output in app.stream(initial_state, config=config):
        for node_name, state_update in output.items():
            print(f" -> Output from {node_name}: {state_update.get('status', '')}")

if __name__ == "__main__":
    # Test execution
    run_antigravity_flow("Initialize standard procedures", "prod-run-001")
