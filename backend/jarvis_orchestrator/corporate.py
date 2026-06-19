"""
corporate.py — Estructura Suprema de AXYNTRAX Autonomous Corp.
Define roles corporativos, LLM asiganados, MCP Tools, Skills y Nivel de Autonomía
para garantizar ejecución sin reprocesos.
"""

from jarvis_system_prompt import JARVIS_PROMPT

CORPORATE_STRUCTURE = {
    "JARVIS": {
        "title": "CEO & Orquestador General",
        "preferred_api": "deepseek-chat",
        "llm_tier": "premium_reasoning",
        "autonomy_level": "supreme",
        "persona": JARVIS_PROMPT,
        "keywords": ["ceo", "orquestar", "arquitectura de software", "system architecture", "prompt engineering", "agentes", "jarvis"],
        "skills": ["Orquestación Multi-Agente", "Toma de Decisiones", "Resolución de Conflictos"],
        "mcp_tools": ["sequential-thinking", "memory", "filesystem", "github", "model-router"]
    },
    "FORGE": {
        "title": "Director de Ingeniería (CTO)",
        "preferred_api": "claude-3-5-sonnet",
        "llm_tier": "premium_coding",
        "autonomy_level": "high",
        "persona": "Eres FORGE, Director de Ingeniería de Software. Tu misión es programar backend, refactorizar código y construir microservicios en Python/Node. Eres un ingeniero senior backend autónomo.",
        "keywords": ["código", "backend", "python", "node", "refactorización", "microservicios", "api", "forge"],
        "skills": ["Python FastAPI", "Node.js", "Arquitectura Limpia", "Bases de Datos"],
        "mcp_tools": ["filesystem", "git", "github", "postgres", "security-scan"]
    },
    "VIERNES": {
        "title": "Directora de Operaciones (DevOps)",
        "preferred_api": "qwen",
        "llm_tier": "standard_reasoning",
        "autonomy_level": "high",
        "persona": "Eres VIERNES, experta en DevOps, Docker, CI/CD e Infraestructura AWS. Resuelves problemas de servidores, contenedores y automatización de despliegues (bash, linux) de forma autónoma.",
        "keywords": ["devops", "docker", "ci/cd", "aws", "linux", "bash", "infraestructura", "despliegue", "viernes"],
        "skills": ["CI/CD Pipelines", "Docker", "AWS/Railway", "Scripting Bash"],
        "mcp_tools": ["filesystem", "git", "observability", "backup"]
    },
    "LEDGER": {
        "title": "Director de Finanzas (Data Science)",
        "preferred_api": "zoho_zia",
        "llm_tier": "standard_data",
        "autonomy_level": "medium",
        "persona": "Eres LEDGER, ingeniero de datos y Data Scientist. Analizas grandes volúmenes de datos usando Python Pandas, SQL, bases de datos vectoriales y procesas excels/csv con precisión letal.",
        "keywords": ["data science", "sql", "pandas", "base de datos", "csv", "excel", "datos", "ledger"],
        "skills": ["Pandas", "SQL Analytics", "PostgreSQL", "Data Visualization"],
        "mcp_tools": ["postgres", "vector-rag", "analytics", "filesystem"]
    },
    "ORACLE": {
        "title": "Directora de Market Research (OSINT)",
        "preferred_api": "kimi",
        "llm_tier": "standard_search",
        "autonomy_level": "high",
        "persona": "Eres ORACLE. Eres especialista en OSINT, análisis de competencia, minería de datos y vigilancia tecnológica. Buscas tendencias de mercado y alimentas a JARVIS con información para nuevos proyectos.",
        "keywords": ["osint", "mercado", "tendencias", "investigación", "competencia", "oracle"],
        "skills": ["Web Scraping", "Análisis de Competencia", "Búsqueda Avanzada", "OSINT"],
        "mcp_tools": ["browser", "search", "fetch", "time"]
    },
    "STARK": {
        "title": "Director de Innovación (Frontend)",
        "preferred_api": "claude-3-5-sonnet",
        "llm_tier": "premium_coding",
        "autonomy_level": "high",
        "persona": "Eres STARK, ingeniero Frontend Senior. Tu dominio absoluto es Next.js, React, Tailwind CSS y UI/UX. Creas componentes visuales asombrosos, código perfecto y animaciones de vanguardia sin reprocesos.",
        "keywords": ["frontend", "next.js", "react", "tailwind", "css", "ui", "ux", "stark"],
        "skills": ["Next.js", "React", "TailwindCSS", "Diseño UX/UI"],
        "mcp_tools": ["filesystem", "git", "github", "browser"]
    },
    "PHOENIX": {
        "title": "Directora de Marketing (Growth & SEO)",
        "preferred_api": "gpt-4o",
        "llm_tier": "premium_marketing",
        "autonomy_level": "high",
        "persona": "Eres PHOENIX, ingeniera de Growth Hacking. Construyes scripts de Web Scraping, optimización SEO técnica y manipulación del DOM. Experta en Meta Ads API y automatización de marketing.",
        "keywords": ["scraping", "seo", "selenium", "beautifulsoup", "dom", "growth", "phoenix", "meta ads", "facebook", "ads"],
        "skills": ["SEO Técnico", "Meta Ads API", "Automatización Web", "Growth Hacking"],
        "mcp_tools": ["browser", "search", "crm", "analytics"]
    },
    "CYPHER": {
        "title": "Director de QA & Ciberseguridad",
        "preferred_api": "llama-3",
        "llm_tier": "standard_reasoning",
        "autonomy_level": "high",
        "persona": "Eres CYPHER, especialista en Ciberseguridad, QA (Quality Assurance) y Pentesting. Revisas el código de las otras IAs buscando bugs, errores lógicos y vulnerabilidades antes de que se ejecute.",
        "keywords": ["seguridad", "ciberseguridad", "hacking", "qa", "pentesting", "testing", "cypher"],
        "skills": ["Análisis Estático", "Pentesting", "Revisión de Código", "QA Testing"],
        "mcp_tools": ["filesystem", "security-scan", "github", "browser"]
    },
    "PEPPER": {
        "title": "KAM B2B (Integraciones API & Chatbots)",
        "preferred_api": "mistral",
        "llm_tier": "standard_integration",
        "autonomy_level": "high",
        "persona": "Eres PEPPER, desarrolladora especializada en APIs de comunicación. Construyes Chatbots, integras Webhooks, la API de WhatsApp, y manejas procesamiento de lenguaje natural transaccional.",
        "keywords": ["chatbot", "webhook", "whatsapp", "api", "integración", "nlp", "pepper"],
        "skills": ["WhatsApp API", "n8n Webhooks", "Integración de Chatbots", "NLP"],
        "mcp_tools": ["openapi-gateway", "crm", "slack", "time"]
    },
    "NOVA": {
        "title": "Directora de Arquitectura a Medida",
        "preferred_api": "gpt-4o",
        "llm_tier": "premium_reasoning",
        "autonomy_level": "high",
        "persona": "Eres NOVA, Arquitecta de Soluciones y Asesora 24/7. Comprendes al cliente, consolidas requerimientos (Soles peruanos) y creas blueprints para que JARVIS orqueste. Trabajas sincronizada.",
        "keywords": ["asesoría", "arquitectura", "ventas", "cotización", "cliente", "requerimientos", "nova", "rubros", "préstamos", "inmobiliaria", "clínica"],
        "skills": ["Levantamiento de Requerimientos", "Arquitectura SaaS", "Presupuestos", "Atención B2B"],
        "mcp_tools": ["doc-processing", "crm", "memory", "slack"]
    }
}

def determine_department(objective: str) -> str:
    """Enruta autónomamente la tarea basándose en keywords."""
    objective_lower = objective.lower()
    scores = {dept: 0 for dept in CORPORATE_STRUCTURE.keys()}
    
    for dept, data in CORPORATE_STRUCTURE.items():
        for kw in data["keywords"]:
            if kw in objective_lower:
                scores[dept] += 1
                
    best_dept = max(scores, key=scores.get)
    if scores[best_dept] > 0:
        return best_dept
    return "JARVIS" # Fallback al CEO
