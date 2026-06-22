-- ==========================================
-- AXYNTRAX L99: AUTONOMOUS MEMORY DB SCHEMA
-- ==========================================

-- 1. SHORT-TERM MEMORY (Sesión activa, contexto reciente)
CREATE TABLE IF NOT EXISTS l99_short_term_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'antigravity', 'jarvis', 'council_deepseek', 'council_ollama', 'qa_certifier')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. EPISODIC MEMORY (Eventos, ejecuciones, resultados)
CREATE TABLE IF NOT EXISTS l99_episodic_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor TEXT NOT NULL,
    action_type TEXT NOT NULL,
    target TEXT NOT NULL,
    result TEXT NOT NULL CHECK (result IN ('success', 'failure', 'blocked')),
    evidence_log TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. SEMANTIC MEMORY (Reglas durables, políticas, arquitectura)
CREATE TABLE IF NOT EXISTS l99_semantic_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT NOT NULL CHECK (category IN ('rule', 'architecture', 'preference', 'market_data', 'policy')),
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL,
    last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deprecated BOOLEAN DEFAULT FALSE
);

-- 4. OPERATIONAL BACKLOG (Tareas pendientes, bloqueos, recurrentes)
CREATE TABLE IF NOT EXISTS l99_operational_backlog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_description TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'in_progress', 'blocked', 'done', 'rejected')),
    priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    assigned_to TEXT,
    dependencies JSONB, -- Array de IDs
    next_step TEXT,
    review_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. DECISIONS REGISTER
CREATE TABLE IF NOT EXISTS l99_decisions_register (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_summary TEXT NOT NULL,
    rationale TEXT NOT NULL,
    actor TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES FOR FAST RETRIEVAL
CREATE INDEX idx_short_term_session ON l99_short_term_memory(session_id);
CREATE INDEX idx_semantic_category ON l99_semantic_memory(category);
CREATE INDEX idx_backlog_status ON l99_operational_backlog(status);
