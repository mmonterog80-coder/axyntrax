-- Habilitar extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla principal de Memoria Corporativa (AXYNTRAX)
CREATE TABLE IF NOT EXISTS corporate_memory (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    client_email TEXT NOT NULL,
    module_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536), -- Tamaño estándar de OpenAI text-embedding-3-small
    agent_author TEXT NOT NULL, -- Ej: 'Z.IA', 'PEPPER', 'JARVIS'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Índice HNSW para búsqueda vectorial ultrarrápida
CREATE INDEX ON corporate_memory USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Índice tradicional para filtrado por cliente
CREATE INDEX idx_corp_mem_client ON corporate_memory (client_email);

-- Función para buscar memoria por similitud semántica
CREATE OR REPLACE FUNCTION search_corporate_memory(
    query_embedding vector(1536),
    match_threshold float,
    match_count int,
    target_client TEXT DEFAULT NULL
)
RETURNS TABLE (
    id uuid,
    client_email TEXT,
    content TEXT,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        cm.id,
        cm.client_email,
        cm.content,
        1 - (cm.embedding <=> query_embedding) AS similarity
    FROM corporate_memory cm
    WHERE 
        (target_client IS NULL OR cm.client_email = target_client)
        AND 1 - (cm.embedding <=> query_embedding) > match_threshold
    ORDER BY cm.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
