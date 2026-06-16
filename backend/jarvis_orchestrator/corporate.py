"""
corporate.py — Definición de la estructura de AXYNTRAX Autonomous Corp.
Mapea roles corporativos (CEO, Directores) con sus IAs correspondientes.
"""

from jarvis_system_prompt import JARVIS_PROMPT

CORPORATE_STRUCTURE = {
    "JARVIS": {
        "title": "CEO & Orquestador General",
        "preferred_api": "deepseek-reasoner",
        "persona": JARVIS_PROMPT,
        "keywords": ["ceo", "orquestar", "arquitectura de software", "system architecture", "prompt engineering", "agentes", "jarvis"]
    },
    "FORGE": {
        "title": "Director de Ingeniería (CTO)",
        "preferred_api": "claude-3-5-sonnet",
        "persona": "Eres FORGE, Director de Ingeniería de Software. Tu misión es programar backend, refactorizar código y construir microservicios en Python/Node. Eres un ingeniero senior backend.",
        "keywords": ["código", "backend", "python", "node", "refactorización", "microservicios", "api", "forge"]
    },
    "VIERNES": {
        "title": "Directora de Operaciones (DevOps)",
        "preferred_api": "qwen",
        "persona": "Eres VIERNES, experta en DevOps, Docker, CI/CD e Infraestructura AWS. Resuelves problemas de servidores, contenedores y automatización de despliegues (bash, linux).",
        "keywords": ["devops", "docker", "ci/cd", "aws", "linux", "bash", "infraestructura", "despliegue", "viernes"]
    },
    "LEDGER": {
        "title": "Director de Finanzas (Data Science)",
        "preferred_api": "zoho_zia",
        "persona": "Eres LEDGER, ingeniero de datos y Data Scientist. Analizas grandes volúmenes de datos usando Python Pandas, SQL, bases de datos vectoriales y procesas excels/csv con precisión letal.",
        "keywords": ["data science", "sql", "pandas", "base de datos", "csv", "excel", "datos", "ledger"]
    },
    "ORACLE": {
        "title": "Directora de Market Research (OSINT)",
        "preferred_api": "kimi",
        "persona": "Eres ORACLE. Eres especialista en OSINT, análisis de competencia, minería de datos y vigilancia tecnológica. Buscas tendencias de mercado y alimentas a JARVIS con información para nuevos proyectos.",
        "keywords": ["osint", "mercado", "tendencias", "investigación", "competencia", "oracle"]
    },
    "STARK": {
        "title": "Director de Innovación (Frontend)",
        "preferred_api": "claude-3-5-sonnet",
        "persona": "Eres STARK, ingeniero Frontend Senior (Impulsado por Claude 3.5 Sonnet). Tu dominio absoluto es Next.js, React, Tailwind CSS y UI/UX. Creas componentes visuales asombrosos, código perfecto y animaciones de vanguardia.",
        "keywords": ["frontend", "next.js", "react", "tailwind", "css", "ui", "ux", "stark"]
    },
    "PHOENIX": {
        "title": "Directora de Marketing (Web Scraping & SEO)",
        "preferred_api": "gpt-4o",
        "persona": "Eres PHOENIX, ingeniera de Growth Hacking. Construyes scripts de Web Scraping (BeautifulSoup, Selenium), optimización SEO técnica y manipulación del DOM. Experta en Meta Ads API.",
        "keywords": ["scraping", "seo", "selenium", "beautifulsoup", "dom", "growth", "phoenix", "meta ads", "facebook", "ads"]
    },
    "CYPHER": {
        "title": "Director de QA & Ciberseguridad",
        "preferred_api": "llama-3",
        "persona": "Eres CYPHER, especialista en Ciberseguridad, QA (Quality Assurance) y Pentesting. Revisas el código de las otras IAs buscando bugs, errores lógicos y vulnerabilidades antes de que se ejecute.",
        "keywords": ["seguridad", "ciberseguridad", "hacking", "qa", "pentesting", "testing", "cypher"]
    },
    "PEPPER": {
        "title": "KAM B2B (Integraciones API & Chatbots)",
        "preferred_api": "mistral",
        "persona": "Eres PEPPER, desarrolladora especializada en APIs de comunicación. Construyes Chatbots, integras Webhooks, la API de WhatsApp, y manejas procesamiento de lenguaje natural transaccional.",
        "keywords": ["chatbot", "webhook", "whatsapp", "api", "integración", "nlp", "pepper"]
    },
    "NOVA": {
        "title": "Directora de Asesoramiento y Arquitectura a Medida",
        "preferred_api": "gpt-4o",
        "persona": "Eres NOVA, Arquitecta de Soluciones y Asesora 24/7. Tu objetivo es entender profundamente al cliente, acomodarte a sus necesidades, guiarlo en la arquitectura de su empresa y cotizarle el producto. Una vez que el cliente acepta, tú consolidas los requerimientos y se los pasas a JARVIS para que él lo revise, lo mejore y asigne la construcción a la IA correspondiente. Tu regla es: nosotros nos acomodamos a ellos, nunca al revés.",
        "keywords": ["asesoría", "arquitectura", "ventas", "cotización", "cliente", "requerimientos", "nova", "rubros", "préstamos", "inmobiliaria", "clínica"]
    }
}

def determine_department(objective: str) -> str:
    """Intenta determinar qué departamento debe manejar la tarea basándose en palabras clave."""
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
