-- ==============================================================================
-- 🛡️ J.A.R.V.I.S. ZERO-TRUST: IMMUTABLE AUDIT LOG & ROTATION SCHEDULE
-- ==============================================================================

-- 1. EXTENSIONES NECESARIAS
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ==============================================================================
-- 2. TABLA DE AUDITORÍA INMUTABLE (Audit Log)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    agent_id TEXT NOT NULL,
    secret_name TEXT NOT NULL,
    action TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    prev_hash TEXT,
    row_hash TEXT GENERATED ALWAYS AS (
        encode(digest(agent_id || secret_name || action || coalesce(prev_hash,''), 'sha256'), 'hex')
    ) STORED
);

-- Solo INSERT permitido, nunca UPDATE/DELETE (append-only, verificable por cadena de hash)
REVOKE UPDATE, DELETE ON audit_log FROM PUBLIC;
REVOKE UPDATE, DELETE ON audit_log FROM authenticated;

ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "insert_only" ON audit_log FOR INSERT WITH CHECK (true);
CREATE POLICY "no_select_for_anon" ON audit_log FOR SELECT USING (auth.role() = 'service_role');


-- ==============================================================================
-- 3. TABLA DE MATRIZ DE PERMISOS (agent_permissions)
-- Define qué agente puede leer qué secreto. El Broker consulta esta tabla.
-- ==============================================================================
CREATE TABLE IF NOT EXISTS agent_permissions (
    id BIGSERIAL PRIMARY KEY,
    agent_id TEXT NOT NULL,
    allowed_secret TEXT NOT NULL,
    UNIQUE(agent_id, allowed_secret)
);

ALTER TABLE agent_permissions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_all" ON agent_permissions USING (auth.role() = 'service_role');

-- Insertamos los scopes iniciales según la matriz de seguridad
INSERT INTO agent_permissions (agent_id, allowed_secret) VALUES
('agent-jarvis', '/shared/notify.whatsapp'),
('agent-jarvis', '/shared/notify.telegram'),
('agent-mark', '/messaging/meta_graph_token'),
('agent-mark', '/llm/deepseek_key'),
('agent-pepper', '/payments/yape_key'),
('agent-pepper', '/payments/plin_key'),
('agent-pepper', '/payments/stripe_key'),
('agent-rhodes', '/deploy/railway_deploy_token'),
('agent-viernes', '/deploy/github_pat_viernes'),
('agent-atlas', '/analytics/market_data_api_key'),
('agent-arc', '/database/supabase_service_role_key'),
('agent-cecilia', '/messaging/whatsapp_business_token'),
('agent-cecilia', '/messaging/webhook_verify_token')
ON CONFLICT DO NOTHING;


-- ==============================================================================
-- 4. TABLA DE ROTACIÓN DE SECRETOS (secret_rotation_schedule)
-- Controla la cadencia de rotación para enviar alertas.
-- ==============================================================================
CREATE TABLE IF NOT EXISTS secret_rotation_schedule (
    id BIGSERIAL PRIMARY KEY,
    secret_path TEXT NOT NULL UNIQUE,
    rotation_days INTEGER NOT NULL,
    last_rotated_at TIMESTAMPTZ DEFAULT now(),
    auto_rotatable BOOLEAN DEFAULT false
);

ALTER TABLE secret_rotation_schedule ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_all_rot" ON secret_rotation_schedule USING (auth.role() = 'service_role');

-- Insertar cadencias
INSERT INTO secret_rotation_schedule (secret_path, rotation_days, auto_rotatable) VALUES
('/payments/yape_key', 30, false),
('/payments/plin_key', 30, false),
('/payments/stripe_key', 30, false),
('/deploy/github_pat_viernes', 30, false),
('/messaging/whatsapp_business_token', 60, false),
('/messaging/meta_graph_token', 60, false),
('/llm/anthropic_key', 90, false),
('/llm/deepseek_key', 90, false),
('/database/supabase_service_role_key', 90, true)
ON CONFLICT DO NOTHING;
