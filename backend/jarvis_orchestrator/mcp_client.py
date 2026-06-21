import asyncio
import json
import os
import logging
from typing import Dict, Any, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger("MCP_Core")
logger.setLevel(logging.INFO)

class MCPOrchestrator:
    def __init__(self, config_path: str = "../../mcp.json"):
        self.config_path = config_path
        self.servers_config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        abs_path = os.path.abspath(self.config_path)
        if not os.path.exists(abs_path):
            logger.warning(f"No se encontro {abs_path}")
            return {}
        with open(abs_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("mcpServers", {})

    async def get_tools_for_server(self, server_name: str):
        if server_name not in self.servers_config:
            raise ValueError(f"Servidor MCP {server_name} no configurado.")
            
        config = self.servers_config[server_name]
        
        env = os.environ.copy()
        if "env" in config:
            env.update(config["env"])
            
        server_params = StdioServerParameters(
            command=config["command"],
            args=config.get("args", []),
            env=env
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    return [tool.model_dump() for tool in tools.tools]
        except Exception as e:
            logger.error(f"Falla al conectar con MCP {server_name}: {e}")
            return []

async def test_mcp():
    orchestrator = MCPOrchestrator(config_path="C:/AXYNTRAX/mcp.json")
    print("Iniciando escaneo de herramientas MCP...")
    try:
        tools = await orchestrator.get_tools_for_server("fetch")
        print("Tools de Fetch:", json.dumps(tools, indent=2))
    except Exception as e:
        print("Error en prueba MCP:", e)

if __name__ == "__main__":
    asyncio.run(test_mcp())
