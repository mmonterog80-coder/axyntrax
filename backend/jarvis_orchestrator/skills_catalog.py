# Creado por: Qwen (Soporte Operativo y Automatización)
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
    dependencies: List[str]

# 20 Skills Predefinidas según el protocolo
DEFAULT_SKILLS = [
    Skill(id="sk_01", name="Prompt Engineering", description="Diseño y optimización de prompts", priority=100, dependencies=[]),
    Skill(id="sk_02", name="Memory Query", description="Acceso a memoria vectorial", priority=90, dependencies=[]),
    Skill(id="sk_03", name="Fact Checking", description="Verificación de hechos contra la web", priority=85, dependencies=[]),
    Skill(id="sk_04", name="Architecture Design", description="Diseño de sistemas", priority=100, dependencies=[]),
    Skill(id="sk_05", name="Code Generation", description="Escritura de código fuente", priority=95, dependencies=["sk_04"]),
    Skill(id="sk_06", name="Debugging", description="Análisis y corrección de bugs", priority=90, dependencies=[]),
    Skill(id="sk_07", name="Refactoring", description="Mejora de estructura de código", priority=80, dependencies=["sk_06"]),
    Skill(id="sk_08", name="Testing and QA", description="Pruebas automáticas", priority=85, dependencies=["sk_05"]),
    Skill(id="sk_09", name="Security Audit", description="Auditoría de seguridad", priority=95, dependencies=["sk_05"]),
    Skill(id="sk_10", name="Market Research", description="Análisis de mercado", priority=60, dependencies=[]),
    Skill(id="sk_11", name="Planning", description="Creación de planes de acción", priority=100, dependencies=[]),
    Skill(id="sk_12", name="Workflow Automation", description="Creación de pipelines", priority=90, dependencies=["sk_11"]),
    Skill(id="sk_13", name="Data Analysis", description="Análisis de datasets", priority=70, dependencies=[]),
    Skill(id="sk_14", name="Data Visualization", description="Generación de gráficos", priority=65, dependencies=["sk_13"]),
    Skill(id="sk_15", name="Documentation", description="Generación de docs técnicos", priority=50, dependencies=[]),
    Skill(id="sk_16", name="Content Writing", description="Redacción de artículos/blogs", priority=40, dependencies=[]),
    Skill(id="sk_17", name="Translation", description="Traducción de idiomas", priority=30, dependencies=[]),
    Skill(id="sk_18", name="API Design", description="Diseño de contratos API", priority=90, dependencies=["sk_04"]),
    Skill(id="sk_19", name="Voice AI", description="Síntesis de voz", priority=50, dependencies=[]),
    Skill(id="sk_20", name="LLM COUNCIL", description="Resolución de problemas críticos por consenso", priority=1000, dependencies=[]),
]

# Catálogo de Herramientas Gratuitas
DEFAULT_TOOLS = [
    Tool(id="t_01", name="FastAPI", category="desarrollo", use_case="APIs rápidas en Python", free_tier="Open Source", limits="Ilimitado", related_skill="sk_18"),
    Tool(id="t_02", name="Railway", category="despliegue", use_case="Hosting de contenedores", free_tier="Developer Plan", limits="500h/mes, 500MB RAM", related_skill="sk_12"),
    Tool(id="t_03", name="Supabase", category="base_de_datos", use_case="PostgreSQL en la nube", free_tier="Free Plan", limits="500MB BDD, 2GB Bandwidth", related_skill="sk_04"),
    Tool(id="t_04", name="Vercel", category="despliegue_frontend", use_case="Hosting frontend", free_tier="Hobby", limits="100GB Bandwidth", related_skill="sk_12"),
    Tool(id="t_05", name="GitHub Actions", category="automatizacion", use_case="CI/CD Pipelines", free_tier="Free", limits="2000 min/mes", related_skill="sk_12")
]
