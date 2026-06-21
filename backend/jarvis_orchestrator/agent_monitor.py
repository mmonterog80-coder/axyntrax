import asyncio
import json
import logging
import os
import time

logger = logging.getLogger(__name__)

class AgentMonitor:
    """Simula o recupera los estados reales de los agentes del escuadrón Axyntrax."""
    
    def __init__(self):
        self.agents = {
            "nanobanana2": {"status": "idle", "current_task": "None", "last_update": time.time(), "cpu": 0, "mem": 0},
            "research": {"status": "idle", "current_task": "None", "last_update": time.time(), "cpu": 0, "mem": 0},
            "jarvis": {"status": "active", "current_task": "Orchestrating", "last_update": time.time(), "cpu": 15, "mem": 45},
            "sentry": {"status": "idle", "current_task": "None", "last_update": time.time(), "cpu": 0, "mem": 0}
        }
        
    def update_agent_status(self, agent_name, status, task):
        if agent_name in self.agents:
            self.agents[agent_name].update({
                "status": status,
                "current_task": task,
                "last_update": time.time(),
                "cpu": 85 if status == "active" else 5,
                "mem": 60 if status == "active" else 10
            })
            
    def get_all_status(self):
        return self.agents
        
# Integración opcional para FastAPI / WebSocket
