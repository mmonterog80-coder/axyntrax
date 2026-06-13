# C:\AXYNTRAX\scripts\setup_and_test.py
import os
import sys
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(dotenv_path=r"C:\AXYNTRAX\.env")
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("ERROR: Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en .env")
    sys.exit(1)

supabase = create_client(url, key)

# --- Intento 1: Insertar sesión directamente ---
try:
    result = supabase.table("agent_sessions").insert({
        "title": "Sesión inicial AXYNTRAX",
        "status": "active"
    }).execute()
    session_id = result.data[0]["id"]
    print("SESSION_ID=" + session_id)
except Exception as e:
    error_msg = str(e)
    print("ERROR_INSERTANDO_SESION: " + error_msg)
    
    # Si el error es porque la tabla no existe, mostrar el SQL necesario
    if "relation" in error_msg.lower() and "does not exist" in error_msg.lower():
        print("TABLAS_NO_EXISTEN")
        print("Por favor, ejecuta manualmente este SQL en el panel de Supabase (SQL Editor):")
        print("""
-- Ve a: https://supabase.com/dashboard/project/qatawtbfrfreakdbluat/sql/new
-- Pega y ejecuta TODO este bloque:

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
        """)
        print("DESPUES_DE_EJECUTAR_EL_SQL: Vuelve a lanzar este mismo script.")
    else:
        print("ERROR_DESCONOCIDO: " + error_msg)
    sys.exit(1)
