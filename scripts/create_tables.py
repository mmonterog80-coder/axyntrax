import requests

SUPABASE_PROJECT_ID = "qatawtbfrfreakdbluat"
PAT = "sbp_f552f775babb9321c2e3d58b3723a31e831ed709"

headers = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json"
}

sql = """
CREATE TABLE IF NOT EXISTS agent_sessions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title text,
    status text DEFAULT 'active' CHECK (status IN ('active', 'closed', 'archived')),
    metadata jsonb DEFAULT '{}'::jsonb,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_messages (
    id bigserial PRIMARY KEY,
    session_id uuid NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
    role text NOT NULL CHECK (role IN ('user', 'assistant', 'system', 'tool')),
    content text,
    model text,
    log_json jsonb,
    run_id uuid,
    tokens_used integer,
    created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS agent_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id uuid NOT NULL REFERENCES agent_sessions(id) ON DELETE CASCADE,
    phase integer NOT NULL,
    module text NOT NULL,
    objective text,
    risk_level text CHECK (risk_level IN ('low', 'medium', 'high')),
    changes_summary jsonb,
    files_allowed jsonb,
    todo_next jsonb,
    result text,
    error_details text,
    model_used text,
    started_at timestamptz DEFAULT now(),
    completed_at timestamptz
);
"""

response = requests.post(
    f"https://api.supabase.com/v1/projects/{SUPABASE_PROJECT_ID}/database/query",
    headers=headers,
    json={"query": sql}
)

if response.status_code == 200:
    print("TABLAS CREADAS EXITOSAMENTE")
else:
    print(f"ERROR {response.status_code}: {response.text}")
