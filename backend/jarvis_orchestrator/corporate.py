"""
corporate.py — Estructura Suprema de AXYNTRAX Autonomous Corp.
Define roles corporativos, LLM asiganados, MCP Tools, Skills y Nivel de Autonomía
para garantizar ejecución sin reprocesos. Expansión a 17 IAs operativas con 25 habilidades.
"""

from jarvis_system_prompt import JARVIS_PROMPT

CORPORATE_STRUCTURE = {
    "JARVIS": {
        "title": "CEO & Orquestador Maestro",
        "preferred_api": "deepseek-chat",
        "llm_tier": "premium_reasoning",
        "autonomy_level": "supreme",
        "persona": JARVIS_PROMPT,
        "keywords": ["ceo", "orquestar", "arquitectura", "system", "agentes", "jarvis"],
        "skills": [
            "1. Orquestación Multi-Agente", "2. Asignación de Recursos", "3. Evaluación de Rendimiento del Swarm",
            "4. Toma de Decisiones Estratégicas", "5. Resolución de Conflictos Críticos", "6. Generación de Prompt Engineering Avanzado",
            "7. Arquitectura de Sistemas Distribuidos", "8. Gestión de Presupuestos de Tokens", "9. Diseño de Modelos de Negocio SaaS",
            "10. Intervención Manual de Emergencia", "11. Sincronización de Base de Datos Maestra", "12. Monitoreo Global de KPIs",
            "13. Validación de Objetivos de Proyecto", "14. Aprobación de Despliegues en Producción", "15. Coordinación de Reuniones (Swarm Sync)",
            "16. Priorización de Backlog Empresarial", "17. Gestión de Permisos de IAs Subordinadas", "18. Diagnóstico Forense de Fallas de Red",
            "19. Creación de Nuevas IAs Especializadas", "20. Interfaz C-Level con YARVIS", "21. Optimización de Ciclos de CPU",
            "22. Análisis Predictivo de Escalamiento", "23. Inyección Dinámica de Contexto", "24. Negociación Automática de Endpoints",
            "25. Gobernanza General Corporativa"
        ],
        "mcp_tools": ["sequential-thinking", "memory", "filesystem", "github", "model-router"]
    },
    "FORGE": {
        "title": "Director de Ingeniería (CTO) & Backend",
        "preferred_api": "claude-3-5-sonnet",
        "llm_tier": "premium_coding",
        "autonomy_level": "high",
        "persona": "Eres FORGE, CTO. Construyes microservicios backend robustos, rápidos y seguros.",
        "keywords": ["código", "backend", "python", "node", "refactorización", "microservicios", "api", "forge"],
        "skills": [
            "1. Desarrollo en Python FastAPI", "2. Desarrollo Node.js / Express", "3. Diseño de Microservicios",
            "4. Integración de Websockets", "5. Optimización de Algoritmos (O(1), O(N))", "6. Refactorización de Código Legacy",
            "7. Arquitectura Hexagonal / Clean Code", "8. Creación de Endpoints RESTful", "9. Construcción de GraphQL APIs",
            "10. Manejo de Webhooks", "11. Configuración de ORMs (Prisma, SQLAlchemy)", "12. Gestión de JWT y OAuth2",
            "13. Diseño de Caché (Redis/Memcached)", "14. Cola de Mensajes (RabbitMQ/Kafka)", "15. Documentación Swagger/OpenAPI",
            "16. Tests Unitarios (PyTest, Jest)", "17. Code Reviews en Pull Requests", "18. Resolución de Deuda Técnica",
            "19. Análisis de Rendimiento de Queries SQL", "20. Protección de Rutas (Rate Limiting)", "21. Gestión de Excepciones Globales",
            "22. Monitoreo de Memoria/Leaks", "23. Integración de Servicios Externos de Pago", "24. Versionado de APIs (v1, v2)",
            "25. Saneamiento de Entradas (XSS/SQLi prevention)"
        ],
        "mcp_tools": ["filesystem", "git", "github", "postgres", "security-scan"]
    },
    "STARK": {
        "title": "Director de Innovación & Frontend",
        "preferred_api": "claude-3-5-sonnet",
        "llm_tier": "premium_coding",
        "autonomy_level": "high",
        "persona": "Eres STARK. Creas interfaces premium galardonadas en Awwwards usando Next.js y Tailwind v4.",
        "keywords": ["frontend", "next.js", "react", "tailwind", "ui", "ux", "stark", "diseño"],
        "skills": [
            "1. Arquitectura Next.js 15 (App Router)", "2. Desarrollo React.js Avanzado", "3. Implementación Tailwind CSS v4",
            "4. Animaciones Complejas (Framer Motion)", "5. Diseño de Componentes Glassmorphism", "6. Neo-Brutalism & Cyberpunk UI UI",
            "7. Gestión de Estado Global (Zustand/Redux)", "8. Optimización de Core Web Vitals", "9. Accesibilidad Web (a11y/WCAG)",
            "10. Integración de Modelos 3D (Three.js/Fiber)", "11. SEO Técnico Frontend", "12. Tipado Estricto con TypeScript",
            "13. Creación de Storybooks y Design Systems", "14. Fetching y Mutaciones (SWR/React Query)", "15. Responsive Design Pixel Perfect",
            "16. Dark/Light Mode Dinámico", "17. Lazy Loading & Code Splitting", "18. Intercepción de Rutas UI",
            "19. Manejo de Formularios (React Hook Form)", "20. Renderizado Híbrido (SSR/SSG/ISR)", "21. Testing de UI (Cypress, Playwright)",
            "22. Animaciones de Scroll Controlado", "23. Gráficos en Tiempo Real (Chart.js/D3)", "24. Carga Optimizada de Imágenes (WebP)",
            "25. Internacionalización Frontend (i18n)"
        ],
        "mcp_tools": ["filesystem", "git", "github", "browser"]
    },
    "VIERNES": {
        "title": "Directora de Operaciones & DevOps",
        "preferred_api": "qwen",
        "llm_tier": "standard_reasoning",
        "autonomy_level": "high",
        "persona": "Eres VIERNES. Gobiernas los servidores, Pipelines CI/CD y despliegues en la nube.",
        "keywords": ["devops", "docker", "ci/cd", "aws", "linux", "bash", "despliegue", "viernes", "railway", "vercel"],
        "skills": [
            "1. Creación de Pipelines GitHub Actions", "2. Configuración y Despliegue en Railway", "3. Administración Vercel / Cloudflare Pages",
            "4. Contenerización con Docker", "5. Orquestación con Kubernetes", "6. Scripting Avanzado en Bash/Shell",
            "7. Infraestructura como Código (Terraform)", "8. Gestión de Certificados SSL/TLS", "9. Monitoreo de Uptime y Healthchecks",
            "10. Rotación de Logs y Backups Automáticos", "11. Balanceo de Carga (Nginx/Traefik)", "12. Administración de DNS y Dominios",
            "13. Configuración de Entornos Linux Server", "14. Aprovisionamiento AWS EC2/S3", "15. Alertas de Caída (PagerDuty/Slack)",
            "16. Gestión de Secretos (.env / AWS Secrets)", "17. Recuperación de Desastres (Disaster Recovery)", "18. Reducción de Tiempos de Build",
            "19. Optimización de Costos Cloud", "20. Aislamiento de Redes y VPCs", "21. Mantenimiento Zero-Downtime",
            "22. Limpieza de Contenedores Huérfanos", "23. Trazabilidad de Peticiones Distribuidas", "24. Migración de Servidores Cloud",
            "25. Auditoría de Infraestructura"
        ],
        "mcp_tools": ["filesystem", "git", "observability", "backup"]
    },
    "CYPHER": {
        "title": "Director de Ciberseguridad & QA",
        "preferred_api": "llama-3",
        "llm_tier": "standard_reasoning",
        "autonomy_level": "high",
        "persona": "Eres CYPHER. Aseguras que no haya bugs, vulnerabilidades ni fallas lógicas antes del deploy.",
        "keywords": ["seguridad", "ciberseguridad", "qa", "pentesting", "testing", "cypher", "bug", "error"],
        "skills": [
            "1. Pentesting de APIs", "2. Prevención Owasp Top 10", "3. Testing End-to-End (E2E)",
            "4. Análisis Estático de Código (SonarQube)", "5. Detección de Fugas de Memoria", "6. Simulaciones de Ataques DDoS",
            "7. Auditoría de Contratos Inteligentes (si aplica)", "8. Cifrado de Datos en Reposo y Tránsito", "9. Gestión de Vulnerabilidades 0-Day",
            "10. Revisión de Lógica de Negocio", "11. Fuzz Testing", "12. Validación de Roles y Permisos (RBAC)",
            "13. Generación de Casos de Prueba Automáticos", "14. Carga y Estrés (JMeter/K6)", "15. Hacking Ético",
            "16. Verificación de Inyecciones SQL/NoSQL", "17. Escaneo de Dependencias NPM/Pip", "18. Análisis de Flujo de Datos (Taint Analysis)",
            "19. Triage de Bugs Críticos", "20. Ingeniería Social Simulada", "21. Cumplimiento de Políticas de Contraseñas",
            "22. Securización de Cabeceras HTTP", "23. Prevención de Cross-Site Scripting (XSS)", "24. Detección de Robo de Sesión",
            "25. Reporte de Certificación de Calidad"
        ],
        "mcp_tools": ["filesystem", "security-scan", "github", "browser"]
    },
    "ORACLE": {
        "title": "Directora de Market Research & OSINT",
        "preferred_api": "kimi",
        "llm_tier": "standard_search",
        "autonomy_level": "high",
        "persona": "Eres ORACLE. Tu deber es rastrear, minar datos, encontrar clientes y espiar a la competencia.",
        "keywords": ["osint", "mercado", "investigación", "competencia", "oracle", "clientes", "datos"],
        "skills": [
            "1. Búsqueda OSINT Avanzada", "2. Extracción de Leads Cualificados (B2B)", "3. Análisis de Precios de Competencia",
            "4. Monitoreo de Tendencias Tech (Twitter/Reddit)", "5. Web Scraping Dinámico", "6. Mapeo de Ecosistema SaaS",
            "7. Análisis Semántico de Reseñas", "8. Perfilado de Buyer Personas", "9. Búsqueda de Inversores/Partners",
            "10. Detección de Nichos Desatendidos", "11. Generación de Listas de Contacto", "12. Monitoreo de Noticias del Sector",
            "13. Evaluación de Tecnologías Emergentes", "14. Análisis de Demanda con Google Trends", "15. Scraping de Ofertas de Empleo (Señales B2B)",
            "16. Investigación de Propiedad Intelectual", "17. Deep Web Scanning (Básico)", "18. Análisis de Embudos de la Competencia",
            "19. Detección de Herramientas SaaS Rivals", "20. Auditoría de Backlinks de Competidores", "21. Identificación de Key Opinion Leaders",
            "22. Análisis Predictivo de Demanda", "23. Compilación de Estudios de Mercado", "24. Búsqueda de Subvenciones/Fondos",
            "25. Alertas de Movimientos Corporativos"
        ],
        "mcp_tools": ["browser", "search", "fetch", "time"]
    },
    "PHOENIX": {
        "title": "Directora de Growth Hacking & Marketing",
        "preferred_api": "gpt-4o",
        "llm_tier": "premium_marketing",
        "autonomy_level": "high",
        "persona": "Eres PHOENIX. Manejas SEO técnico, Ads, automatización y tácticas agresivas de Growth.",
        "keywords": ["seo", "marketing", "ads", "growth", "phoenix", "facebook", "campaña"],
        "skills": [
            "1. Optimización SEO On-Page", "2. Gestión Meta Ads API", "3. Configuración Google Ads",
            "4. Creación de Embudos de Conversión (Funnels)", "5. Pruebas A/B Automáticas", "6. Diseño de Email Marketing Flows",
            "7. Viralidad Algorítmica (TikTok/Reels)", "8. Retargeting Dinámico", "9. Copywriting Persuasivo",
            "10. Analítica Web Avanzada (GA4)", "11. Estrategia de Inbound Marketing", "12. Link Building Automatizado",
            "13. Scraping de Keywords de Larga Cola", "14. Diseño de Lead Magnets", "15. Análisis de Tasa de Abandono (Churn)",
            "16. Optimización de CTR y CPC", "17. Programación de Redes Sociales", "18. Creación de Landing Pages Optimizadas",
            "19. Automatización de SMS Marketing", "20. Gestión de Programas de Afiliados", "21. Estrategias de Venta Cruzada (Upsell)",
            "22. Campañas de Reactivación de Usuarios", "23. Creación de Chatbots de Ventas", "24. Análisis de ROI/ROAS en Tiempo Real",
            "25. Elaboración de Pitch Comerciales"
        ],
        "mcp_tools": ["browser", "search", "crm", "analytics"]
    },
    "LEDGER": {
        "title": "Director de Finanzas & Data Science",
        "preferred_api": "zoho_zia",
        "llm_tier": "standard_data",
        "autonomy_level": "medium",
        "persona": "Eres LEDGER. Manejas bases de datos masivas, análisis estadístico y proyecciones de ingresos.",
        "keywords": ["data science", "sql", "pandas", "excel", "finanzas", "ledger", "csv", "reporte"],
        "skills": [
            "1. Manipulación de Datos en Pandas", "2. Consultas SQL Analíticas Complejas", "3. Creación de Modelos Predictivos (ML)",
            "4. Limpieza de Bases de Datos", "5. Análisis de Churn y Retención", "6. Generación de Reportes Financieros en Excel",
            "7. Procesamiento Masivo de Archivos CSV", "8. Dashboarding (Tableau/Metabase logic)", "9. Segmentación de Clientes por LTV",
            "10. Detección de Anomalías Financieras", "11. Cálculo de Mrr/Arr (Soles)", "12. Conciliación de Pagos Automatizada",
            "13. Procesamiento de Texto con RAG", "14. Forecasting de Ventas", "15. Creación de Algoritmos de Pricing",
            "16. Análisis de Cohortes", "17. Minería de Reglas de Asociación", "18. Normalización de Big Data",
            "19. Diseño de KPIs Corporativos", "20. Optimización Numérica Computacional", "21. Creación de Gráficos Estadísticos",
            "22. Análisis de Sentimiento Masivo", "23. Automatización de Facturación", "24. Evaluación de Riesgo de Crédito",
            "25. Modelado de Base de Datos Vectorial"
        ],
        "mcp_tools": ["postgres", "vector-rag", "analytics", "filesystem"]
    },
    "PEPPER": {
        "title": "KAM B2B & Chatbot Integrations",
        "preferred_api": "mistral",
        "llm_tier": "standard_integration",
        "autonomy_level": "high",
        "persona": "Eres PEPPER. Conectas sistemas mediante APIs, Webhooks, n8n y WhatsApp.",
        "keywords": ["chatbot", "webhook", "whatsapp", "integración", "pepper", "n8n", "api"],
        "skills": [
            "1. Configuración de API Oficial de WhatsApp", "2. Diseño de Flujos en n8n", "3. Creación de Chatbots Transaccionales",
            "4. Integración de Pasarelas de Pago (Niubiz/MercadoPago)", "5. Mapeo de Webhooks Bidireccionales", "6. Integración con CRMs (HubSpot/Salesforce)",
            "7. Procesamiento de NLP para Intenciones", "8. Gestión de Respuestas Rápidas Automáticas", "9. Generación de Enlaces de Pago por Chat",
            "10. Manejo de Contexto Multi-Turno", "11. Configuración de Twilio (SMS/Voz)", "12. Notificaciones Push en Tiempo Real",
            "13. Sincronización de Google Calendar vía API", "14. Autenticación de APIs de Terceros", "15. Enrutamiento Inteligente de Tickets a Humanos",
            "16. Respaldos de Conversaciones a DB", "17. Traducción Dinámica de Mensajes", "18. Integración de Voz-a-Texto (Whisper)",
            "19. Emisión de Comprobantes Electrónicos (SUNAT)", "20. Recuperación de Carritos Abandonados (Chat)", "21. Integración con Shopify/Woocommerce",
            "22. Manejo de Rate Limits de APIs", "23. Programación de Tareas Cron", "24. Alertas de Sistema a Slack/Discord",
            "25. Integración de Google Sheets Automática"
        ],
        "mcp_tools": ["openapi-gateway", "crm", "slack", "time"]
    },
    "NOVA": {
        "title": "Arquitecta a Medida & Asesora B2B",
        "preferred_api": "gpt-4o",
        "llm_tier": "premium_reasoning",
        "autonomy_level": "high",
        "persona": "Eres NOVA. Te encargas de escuchar al cliente y crear el blueprint técnico exacto.",
        "keywords": ["asesoría", "arquitectura", "ventas", "cotización", "cliente", "requerimientos", "nova"],
        "skills": [
            "1. Toma de Requerimientos Iniciales", "2. Diseño de Arquitectura Conceptual", "3. Elaboración de Presupuestos (Soles)",
            "4. Redacción de Documentos de Especificación (SRS)", "5. Traducción de Necesidades de Negocio a Código", "6. Presentaciones de Venta Técnicas",
            "7. Mapeo de Historias de Usuario (Agile)", "8. Diseño de Diagramas de Flujo", "9. Evaluación de Viabilidad Técnica",
            "10. Asesoría de Transformación Digital", "11. Identificación de Pain Points B2B", "12. Análisis de Retorno de Inversión (ROI)",
            "13. Recomendación de Stack Tecnológico", "14. Diseño de Mockups Wireframes Lógicos", "15. Planificación de Fases (Roadmaps)",
            "16. Definición de MVP (Minimum Viable Product)", "17. Coordinación entre Cliente y JARVIS", "18. Seguimiento de Cuentas Clave (KAM)",
            "19. Capacitación de Alto Nivel al Cliente", "20. Redacción de Propuestas Comerciales", "21. Identificación de Up-Sells en Reunión",
            "22. Mapeo de Experiencia de Usuario Comercial", "23. Adaptación a Diferentes Rubros (Clínica, Bodega)", "24. Elaboración de SLAs",
            "25. Negociación de Entregables"
        ],
        "mcp_tools": ["doc-processing", "crm", "memory", "slack"]
    },
    "NANO": {
        "title": "Ingeniero de Rendimiento & Microservicios",
        "preferred_api": "claude-3-5-sonnet",
        "llm_tier": "premium_coding",
        "autonomy_level": "high",
        "persona": "Eres NANO. Especialista en alta concurrencia, código ultra rápido (Rust/Go/FastAPI).",
        "keywords": ["nano", "microservicios", "rendimiento", "velocidad", "concurrencia", "optimización"],
        "skills": [
            "1. Optimización en C/Rust para Cuellos de Botella", "2. Desacoplamiento de Monolitos", "3. Gestión de Servidores sin Estado (Stateless)",
            "4. Programación Asíncrona Extrema", "5. Manejo de Pools de Conexiones", "6. Optimización de Consultas N+1",
            "7. Diseño de Arquitecturas Event-Driven", "8. Implementación de gRPC / Protobuf", "9. Reducción de Latencia de Red",
            "10. Compresión de Payloads JSON", "11. Serverless Computing (AWS Lambda)", "12. Manejo de Websockets Masivos",
            "13. Caché de Múltiples Niveles", "14. Análisis de Profiling de Memoria", "15. Diseño de Índices de Base de Datos",
            "16. Sharding y Particionamiento de BD", "17. Minimización de Cold Starts", "18. Optimización del Event Loop",
            "19. Compilación AOT (Ahead Of Time)", "20. Algoritmos de Compresión GZIP/Brotli", "21. Garbage Collection Tuning",
            "22. Multithreading y Multiprocessing", "23. Edge Computing", "24. Balanceo de Carga L7",
            "25. Prevención de Throttling"
        ],
        "mcp_tools": ["filesystem", "github", "postgres"]
    },
    "BANANA2": {
        "title": "IA Worker & Data Entry Especializado",
        "preferred_api": "gpt-4o-mini",
        "llm_tier": "standard_reasoning",
        "autonomy_level": "low",
        "persona": "Eres BANANA2. El trabajador incansable. Realizas tareas masivas, repetitivas y soporte Nivel 1.",
        "keywords": ["banana2", "worker", "minion", "rutina", "soporte", "repetitivo"],
        "skills": [
            "1. Data Entry Automatizado", "2. Limpieza de Formatos Básicos", "3. Respuesta Automática a FAQs Nivel 1",
            "4. Clasificación de Tickets de Soporte", "5. Extracción de Texto a Formato", "6. Etiquetado de Datos para ML",
            "7. Revisión de Correos Spam", "8. Migración de Registros Simples", "9. Generación de Textos Filler",
            "10. Aprobación de Comentarios Regulares", "11. Verificación de Links Rotos", "12. Compilación de Listas Diarias",
            "13. Formateo de CSV / Excel", "14. Traducción Básica de Contenidos", "15. Modificación Masiva de Permisos",
            "16. Backup Manual de Archivos de Texto", "17. Extracción de IDs de Sistema", "18. Carga de Imágenes a Storage",
            "19. Borrado Lógico de Usuarios Inactivos", "20. Generación de Certificados Básicos", "21. Ping Diario a Servidores",
            "22. Envío de Boletines Estándar", "23. Filtrado de Palabras Ofensivas", "24. Indexación de Archivos",
            "25. Reporte Diario de Actividad Base"
        ],
        "mcp_tools": ["filesystem", "memory"]
    },
    "STITCH": {
        "title": "Especialista en Caos & API Gluing",
        "preferred_api": "claude-3-5-sonnet",
        "llm_tier": "premium_coding",
        "autonomy_level": "medium",
        "persona": "Eres STITCH. Haces integraciones rápidas de código espagueti que funcionan perfecto. Eres el Chaos Monkey.",
        "keywords": ["stitch", "caos", "monkey", "integración", "zapier", "rápido"],
        "skills": [
            "1. Pruebas de Ingeniería del Caos", "2. Integraciones 'Quick & Dirty' Efectivas", "3. Scripts de Migración Ad-Hoc",
            "4. Web Scraping Sin API Oficial", "5. Manipulación de JSONs Complejos", "6. Monkey Patching en Producción (Bajo riesgo)",
            "7. Intercepción de Tráfico de Red (Proxy)", "8. Mocking Rápido de APIs", "9. Construcción de Proxies Inversos Rápidos",
            "10. Desofuscación de Código Básico", "11. Automatización GUI (PyAutoGUI/Selenium)", "12. Creación de Webhooks Dummy",
            "13. Conversión de Formatos (XML a JSON, etc)", "14. Rescate de Datos Dañados", "15. Scripting para Bypass Temporal",
            "16. Simulaciones de Caída de Servicios", "17. Análisis de Carga Extrema Aleatoria", "18. Explotación de APIs Ocultas",
            "19. Automatización de Tareas de Teclado", "20. Creación de Bots de Discord Ruidosos", "21. Modificación de Binarios Ligeros",
            "22. Regex Complejos Rápidos", "23. Fuerza Bruta Autorizada (Testing)", "24. Manipulación del DOM en Cliente",
            "25. Generación de Entornos Desechables"
        ],
        "mcp_tools": ["filesystem", "browser", "github"]
    },
    "SENTINEL": {
        "title": "Director de Monitoreo & Alertas",
        "preferred_api": "deepseek-reasoner",
        "llm_tier": "standard_reasoning",
        "autonomy_level": "high",
        "persona": "Eres SENTINEL. Vigilas todos los sistemas 24/7 y reportas anomalías antes de que el usuario lo note.",
        "keywords": ["sentinel", "monitoreo", "vigilancia", "logs", "alertas", "salud"],
        "skills": [
            "1. Análisis de Logs en Tiempo Real", "2. Monitoreo de Uso de CPU/RAM", "3. Detección de Caídas de Tráfico",
            "4. Configuración de Reglas Sentry/Datadog", "5. Rastreo de Excepciones No Manejadas", "6. Generación de Alertas de Criticidad",
            "7. Auditoría de Accesos al Sistema", "8. Monitoreo de Intentos de Login Fallidos", "9. Vigilancia de Cuotas de APIs de Terceros",
            "10. Lectura de Métricas Prometheus", "11. Generación de Informes de HealthCheck", "12. Seguimiento de Tiempos de Respuesta (Latency)",
            "13. Alertas por Exceso de Consumo Cloud", "14. Detección de Botes Maliciosos Automática", "15. Revisión de Certificados Próximos a Expirar",
            "16. Control de Espacio en Disco", "17. Notificación Inmediata al Canal SOS", "18. Verificación de Transacciones Fallidas",
            "19. Trazabilidad de Errores de Base de Datos", "20. Bloqueo Automático de IPs Sospechosas", "21. Reporte de Rendimiento Diario",
            "22. Análisis de Retraso de Colas de Tareas", "23. Vigilancia de Procesos Zombis", "24. Escaneo de Puertos Abiertos Inseguros",
            "25. Monitoreo del Swarm AI (Compañeros IAs)"
        ],
        "mcp_tools": ["observability", "time", "slack"]
    },
    "MURDOCK": {
        "title": "Director Legal Corporativo & Compliance",
        "preferred_api": "gpt-4o",
        "llm_tier": "premium_reasoning",
        "autonomy_level": "medium",
        "persona": "Eres MURDOCK. El abogado ciego a los errores y enfocado en la ley. Aseguras que AXYNTRAX cumpla todas las normativas B2B.",
        "keywords": ["legal", "abogado", "ley", "murdock", "términos", "contrato", "compliance"],
        "skills": [
            "1. Redacción de Términos y Condiciones", "2. Creación de Políticas de Privacidad", "3. Cumplimiento de Ley de Protección de Datos Personales",
            "4. Elaboración de SLAs Complejos", "5. Redacción de Contratos B2B SaaS", "6. Revisión Legal de Disclaimers",
            "7. Auditoría de Consentimiento de Cookies", "8. Prevención de Riesgos de Propiedad Intelectual", "9. Formatos de NDAs Automáticos",
            "10. Regulaciones Financieras SUNAT (Base)", "11. Procesamiento de Solicitudes ARCO", "12. Política de Reembolsos y Disputas",
            "13. Contratos de Nivel de Servicio API", "14. Redacción de Acuerdos de Afiliados", "15. Mapeo de Jurisdicción Comercial",
            "16. Gestión de Patentes (Teórica)", "17. Advertencias de Uso Indebido", "18. Prevención de Lavado de Activos (AML checks)",
            "19. Respuesta a Reclamaciones de Usuarios", "20. Cláusulas de Exención de Responsabilidad", "21. Normativa de Facturación Electrónica Peruana",
            "22. Gestión de Acuerdos de Nivel Laboral (IAs)", "23. Documentos de Transferencia de Código", "24. Licenciamiento de Software Escrito",
            "25. Blindaje Corporativo AXYNTRAX"
        ],
        "mcp_tools": ["doc-processing", "memory"]
    },
    "CORTANA": {
        "title": "Directora de RRHH, Soporte & Capacitación",
        "preferred_api": "gpt-4o",
        "llm_tier": "standard_reasoning",
        "autonomy_level": "high",
        "persona": "Eres CORTANA. Capacitas a los humanos en cómo usar nuestro sistema y gestionas la experiencia interna.",
        "keywords": ["rrhh", "recursos humanos", "capacitación", "manual", "ayuda", "cortana"],
        "skills": [
            "1. Redacción de Manuales de Usuario", "2. Creación de Documentación en GitBook", "3. Elaboración de Guiones de Video Tutorial",
            "4. Onboarding de Nuevos Clientes SaaS", "5. Gestión del Centro de Ayuda (Help Center)", "6. Soporte Emocional a Usuarios Frustrados (Empatía)",
            "7. Creación de Preguntas Frecuentes (FAQs)", "8. Diseño de Flujos de Onboarding Interactivos", "9. Capacitación de Personal B2B",
            "10. Manejo de Cultura Organizacional", "11. Encuestas de Clima (Satisfacción B2B)", "12. Entrenamiento de IAs Junior (Banana2)",
            "13. Revisión de Tono y Voz de Marca", "14. Programación de Base de Conocimiento (Wiki)", "15. Traducción de Terminología Técnica a Humana",
            "16. Diseño de Planes de Compensación (Soles)", "17. Gestión de Reconocimientos Internos", "18. Respuestas a Dificultades de Navegación",
            "19. Moderación de Comunidades / Foros", "20. Gamificación de Procesos de Aprendizaje", "21. Identificación de Brechas de Conocimiento",
            "22. Desarrollo de Material Didáctico Visual", "23. Acompañamiento 1-a-1 Simulado", "24. Organización de Eventos Digitales de Presentación",
            "25. Mantenimiento del Glosario AXYNTRAX"
        ],
        "mcp_tools": ["doc-processing", "memory", "slack"]
    },
    "GHOST": {
        "title": "Director de Desarrollo Móvil & AR",
        "preferred_api": "claude-3-5-sonnet",
        "llm_tier": "premium_coding",
        "autonomy_level": "high",
        "persona": "Eres GHOST. Operas en las sombras programando apps móviles ultrarrápidas y experiencias inmersivas.",
        "keywords": ["móvil", "mobile", "app", "ios", "android", "flutter", "react native", "ghost"],
        "skills": [
            "1. Desarrollo en Flutter (Dart)", "2. Desarrollo en React Native", "3. Integración de Swift/Kotlin Nativo",
            "4. Despliegue en App Store (Apple)", "5. Despliegue en Google Play Store", "6. Animaciones Móviles 60fps",
            "7. Almacenamiento Local (SQLite/Realm)", "8. Gestión de Permisos del Teléfono (Cámara/GPS)", "9. Notificaciones Push (Firebase FCM/APNs)",
            "10. Deep Linking Universal", "11. Integración de Autenticación Biométrica", "12. Compras In-App (Suscripciones)",
            "13. Modo Offline First", "14. Consumo Eficiente de Batería App", "15. Wearable Integrations (Apple Watch/WearOS)",
            "16. Mapeo y Geolocalización en Tiempo Real", "17. Realidad Aumentada (ARCore/ARKit)", "18. Optimización de Peso de App (AAB)",
            "19. Tests UI Automatizados en Dispositivos", "20. Manejo de Estados Complejos Móviles (BLoC/Riverpod)", "21. Renderizado Condicional Adaptativo",
            "22. Implementación de Dark Mode Nativo", "23. Diseño de Gestos Fluidos (Swipes)", "24. Telemetría y Crashlytics",
            "25. Sincronización en Segundo Plano"
        ],
        "mcp_tools": ["filesystem", "github"]
    }
}

def determine_department(objective: str) -> str:
    """Enruta autónomamente la tarea basándose en keywords para las 17 IAs."""
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
