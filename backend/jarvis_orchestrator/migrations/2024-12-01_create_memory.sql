-- Enable pgvector extension (Supabase provides it)
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS memory (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL, -- OpenAI text-embedding-3-small returns 1536 dimensions
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast similarity search
CREATE INDEX IF NOT EXISTS idx_memory_embedding ON memory USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
