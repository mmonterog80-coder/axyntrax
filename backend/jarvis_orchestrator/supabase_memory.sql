-- ==============================================================================
-- 🧠 J.A.R.V.I.S. MARK X: CORPORATE MEMORY MODULE (pgvector)
-- ==============================================================================

-- 1. Habilitar extensión vectorial
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Crear la tabla de memoria corporativa permanente
CREATE TABLE IF NOT EXISTS corporate_memory (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT, -- Para agrupar recuerdos de un mismo cliente o proyecto
    agent_id TEXT, -- ¿Quién registró este recuerdo? (gemini, deepseek, zia)
    content TEXT NOT NULL, -- El recuerdo en texto plano (ej. "El cliente prefiere Tailwind oscuro")
    metadata JSONB, -- Contexto adicional (fecha, tags, urls)
    embedding vector(1536), -- Vector numérico (ej. de text-embedding-ada-002 o equivalente)
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Crear índice para búsquedas semánticas rápidas (HNSW)
-- Usamos el operador de distancia del producto interno (inner product)
CREATE INDEX IF NOT EXISTS corporate_memory_embedding_idx 
ON corporate_memory USING hnsw (embedding vector_ip_ops);

-- 4. Seguridad (Row Level Security)
ALTER TABLE corporate_memory ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_all_memory" ON corporate_memory USING (auth.role() = 'service_role');
REVOKE ALL ON corporate_memory FROM PUBLIC;
REVOKE ALL ON corporate_memory FROM authenticated;
