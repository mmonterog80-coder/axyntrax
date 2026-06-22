-- Crear tabla de cola de tareas
CREATE TABLE IF NOT EXISTS task_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_name TEXT NOT NULL,
    task_data JSONB NOT NULL,
    assigned_agent TEXT,
    priority INTEGER DEFAULT 3, -- P0=0, P1=1, P2=2, P3=3, P4=4
    status TEXT DEFAULT 'pending', -- pending, in_progress, completed, failed
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    error_message TEXT,
    result JSONB
);

-- Crear índice para consultas rápidas
CREATE INDEX IF NOT EXISTS idx_task_queue_status_priority ON task_queue(status, priority);

-- Función para tomar la siguiente tarea
CREATE OR REPLACE FUNCTION get_next_task(agent_name TEXT)
RETURNS TABLE (task_id UUID, task_name TEXT, task_data JSONB) AS $$
BEGIN
    UPDATE task_queue
    SET status = 'in_progress', assigned_agent = agent_name, updated_at = NOW()
    WHERE id = (
        SELECT id FROM task_queue
        WHERE status = 'pending'
        ORDER BY priority ASC, created_at ASC
        LIMIT 1
    )
    RETURNING id, task_queue.task_name, task_queue.task_data INTO task_id, task_name, task_data;
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

-- Función para reportar resultado
CREATE OR REPLACE FUNCTION complete_task(task_id UUID, task_result JSONB, task_error TEXT DEFAULT NULL)
RETURNS VOID AS $$
BEGIN
    UPDATE task_queue
    SET status = CASE WHEN task_error IS NULL THEN 'completed' ELSE 'failed' END,
        result = task_result,
        error_message = task_error,
        updated_at = NOW()
    WHERE id = task_id;
END;
$$ LANGUAGE plpgsql;

-- Crear tabla de logs de agentes
CREATE TABLE IF NOT EXISTS agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_name TEXT NOT NULL,
    task_id UUID REFERENCES task_queue(id),
    timestamp TIMESTAMP DEFAULT NOW(),
    status TEXT NOT NULL, -- 'started', 'in_progress', 'completed', 'failed'
    data JSONB,
    error_message TEXT,
    artifact_urls TEXT[],
    duration_ms INTEGER,
    next_step TEXT
);

-- Crear índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_agent_logs_agent_timestamp ON agent_logs(agent_name, timestamp DESC);
