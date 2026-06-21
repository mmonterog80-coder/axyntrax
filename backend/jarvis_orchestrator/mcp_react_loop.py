import json
import os
import asyncio
from openai import OpenAI
from mcp_client import MCPOrchestrator

orchestrator = MCPOrchestrator(config_path="C:/AXYNTRAX/mcp.json")

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "list_mcp_tools",
            "description": "Devuelve la lista de herramientas disponibles en un servidor MCP específico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "server_name": {
                        "type": "string",
                        "description": "Nombre del servidor MCP (ej: 'github', 'postgres', 'browser', 'fetch', 'sentry', 'redis')"
                    }
                },
                "required": ["server_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_mcp_tool",
            "description": "Ejecuta una herramienta en un servidor MCP.",
            "parameters": {
                "type": "object",
                "properties": {
                    "server_name": {
                        "type": "string"
                    },
                    "tool_name": {
                        "type": "string"
                    },
                    "arguments": {
                        "type": "string",
                        "description": "Diccionario JSON en formato string con los argumentos"
                    }
                },
                "required": ["server_name", "tool_name", "arguments"]
            }
        }
    }
]

def run_sync_mcp_list(server_name):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(orchestrator.get_tools_for_server(server_name))

def run_sync_mcp_call(server_name, tool_name, args):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(orchestrator.call_tool(server_name, tool_name, args))

def call_deepseek(user_message: str) -> str:
    from telegram_handler import llm_response_cache, logger, JARVIS_TELEGRAM_PROMPT
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        return "Señor Miguel, el enlace con DeepSeek no está disponible."
    
    client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
    messages = [
        {"role": "system", "content": JARVIS_TELEGRAM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    
    # Bucle ReAct (hasta 5 iteraciones)
    for _ in range(5):
        try:
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                tools=tools_schema,
                max_tokens=500
            )
            msg = resp.choices[0].message
            messages.append(msg)
            
            if not msg.tool_calls:
                return msg.content.strip()
                
            for tool_call in msg.tool_calls:
                args = json.loads(tool_call.function.arguments)
                tool_result = ""
                
                if tool_call.function.name == "list_mcp_tools":
                    tools = run_sync_mcp_list(args["server_name"])
                    tool_result = json.dumps(tools)
                elif tool_call.function.name == "run_mcp_tool":
                    mcp_args = json.loads(args["arguments"]) if isinstance(args["arguments"], str) else args["arguments"]
                    res = run_sync_mcp_call(args["server_name"], args["tool_name"], mcp_args)
                    tool_result = json.dumps(res)
                    
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)[:2000] # Limitar a 2000 chars
                })
        except Exception as e:
            logger.error(f"DeepSeek MCP loop error: {e}")
            return f"Señor, ocurrió un error interno al ejecutar el flujo MCP: {str(e)}"
            
    return "Señor, he superado el límite de operaciones lógicas. Deteniendo ejecución por seguridad."
