from pydantic import BaseModel
from typing import List, Optional

class Tool(BaseModel):
    id: str
    name: str
    category: str
    use_case: str
    free_tier: str
    limits: str
    related_skill: str

class Skill(BaseModel):
    id: str
    name: str
    description: str
    priority: int
    assigned_agent: str
    tier: str
    dependencies: List[str]

# 10 Master Skills - MARK X
DEFAULT_SKILLS = [
    Skill(id="sk_01", name="Lead Generation B2B", description="Zia + Gemini escanean internet y redes buscando clientes.", priority=100, assigned_agent="zia", tier="strategy", dependencies=[]),
    Skill(id="sk_02", name="Market Analysis", description="Kimi y Gemini analizan la competencia y estructuran propuestas visuales.", priority=90, assigned_agent="kimi", tier="strategy", dependencies=["sk_01"]),
    Skill(id="sk_03", name="Voice Pitching", description="Fish Audio y ElevenLabs sintetizan notas de voz perfectas para enviar por Meta/WhatsApp.", priority=80, assigned_agent="fish_audio", tier="strategy", dependencies=["sk_02"]),
    
    Skill(id="sk_04", name="Architecture Design", description="Gemini diseña la base de datos Supabase y la arquitectura de nube.", priority=100, assigned_agent="jarvis", tier="engineering", dependencies=["sk_02"]),
    Skill(id="sk_05", name="Frontend Weaver", description="Stitch y Kimi generan código React/Three.js de ultra alta calidad.", priority=90, assigned_agent="stitch", tier="engineering", dependencies=["sk_04"]),
    Skill(id="sk_06", name="Backend Forge", description="DeepSeek V4 Flash / Coder programan la API y lógica dura.", priority=90, assigned_agent="forge", tier="engineering", dependencies=["sk_04"]),
    Skill(id="sk_07", name="Code Review & Security", description="Baidu Ernie 4.0 / Yi-34B revisan el código buscando vulnerabilidades.", priority=80, assigned_agent="sentinel", tier="engineering", dependencies=["sk_05", "sk_06"]),
    
    Skill(id="sk_08", name="Cloud Deploy", description="Qwen3 Max gestiona Railway/Vercel y hace el push a producción.", priority=100, assigned_agent="devops_ai", tier="operations", dependencies=["sk_07"]),
    Skill(id="sk_09", name="Telegram Reporting", description="Telegram Bot envía notificaciones al CEO de despliegues y pagos.", priority=90, assigned_agent="jarvis", tier="operations", dependencies=["sk_08"]),
    Skill(id="sk_10", name="Continuous Memory Sync", description="JARVIS guarda todo el contexto en Supabase pgvector.", priority=100, assigned_agent="jarvis", tier="operations", dependencies=[])
]

# Catálogo de Herramientas (Broker)
DEFAULT_TOOLS = [
    Tool(id="t_01", name="FastAPI", category="desarrollo", use_case="APIs rápidas en Python", free_tier="Open Source", limits="Ilimitado", related_skill="sk_06"),
    Tool(id="t_02", name="Railway", category="despliegue", use_case="Hosting de contenedores", free_tier="Developer Plan", limits="500h/mes", related_skill="sk_08"),
    Tool(id="t_03", name="Supabase pgvector", category="base_de_datos", use_case="Memoria permanente y Vector DB", free_tier="Free Plan", limits="500MB BDD", related_skill="sk_10"),
    Tool(id="t_04", name="Vercel", category="despliegue_frontend", use_case="Hosting frontend UI", free_tier="Hobby", limits="100GB Bandwidth", related_skill="sk_08"),
    Tool(id="t_05", name="Infisical", category="seguridad", use_case="Vault de Secretos Zero-Trust", free_tier="Free", limits="Proyectos limitados", related_skill="sk_07")
]

SKILLS_CATALOG = {
    "skills": [s.dict() for s in DEFAULT_SKILLS],
    "tools": [t.dict() for t in DEFAULT_TOOLS]
}
