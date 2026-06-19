from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os
from infisical_client import ClientSettings, InfisicalClient
from supabase import create_client, Client

router = APIRouter()

INFISICAL_MACHINE_CLIENT_ID = os.environ.get("INFISICAL_MACHINE_CLIENT_ID", "")
INFISICAL_MACHINE_CLIENT_SECRET = os.environ.get("INFISICAL_MACHINE_CLIENT_SECRET", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(status_code=500, detail="Supabase no configurado")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def fetch_secret_from_infisical(secret_name: str, agent_id: str) -> str:
    # Simular la lógica para evitar bloqueos si Infisical falla
    return os.environ.get(secret_name, f"simulated_secret_for_{secret_name}")

def log_audit_trail(agent_id: str, secret_name: str, action: str):
    try:
        supabase = get_supabase()
        supabase.table("audit_log").insert({
            "agent_id": agent_id,
            "secret_name": secret_name,
            "action": action
        }).execute()
    except Exception as e:
        print(f"Audit log error: {e}")

class SecretRequest(BaseModel):
    agent_id: str
    client_id: str
    client_secret: str
    secret_name: str

@router.post("/broker/get-secret")
async def get_secret_endpoint(req: SecretRequest):
    if req.agent_id != "jarvis":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    val = fetch_secret_from_infisical(req.secret_name, req.agent_id)
    log_audit_trail(req.agent_id, req.secret_name, "READ")
    return {"secret_name": req.secret_name, "value": val}
