from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
import os
import time
from infisical_sdk import InfisicalSDKClient
# Asumiendo que usas supabase client oficial: supabase-py
from supabase import create_client, Client

router = APIRouter()

# Supabase Client Init
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
except Exception:
    supabase = None

# Infisical Client Init (Master Identity)
infisical_client = None
try:
    if os.environ.get("BROKER_MASTER_CLIENT_ID"):
        infisical_client = InfisicalSDKClient(host="https://app.infisical.com")
        infisical_client.auth.universal_auth.login(
            client_id=os.environ.get("BROKER_MASTER_CLIENT_ID"),
            client_secret=os.environ.get("BROKER_MASTER_CLIENT_SECRET"),
        )
except Exception as e:
    print("Error conectando con Infisical (Master Broker):", e)


class SecretRequest(BaseModel):
    agent_id: str
    client_id: str
    client_secret: str
    path: str
    name: str

def log_audit(agent_id: str, secret_name: str, action: str):
    if not supabase: return
    try:
        supabase.table("audit_log").insert({
            "agent_id": agent_id,
            "secret_name": secret_name,
            "action": action
        }).execute()
    except Exception as e:
        print("Error registrando auditoria:", e)

def verify_agent_identity(agent_id: str, client_id: str, client_secret: str) -> bool:
    """Valida que el agente sea quien dice ser autenticando contra Infisical (Universal Auth)"""
    try:
        temp_client = InfisicalSDKClient(host="https://app.infisical.com")
        temp_client.auth.universal_auth.login(
            client_id=client_id,
            client_secret=client_secret
        )
        return True
    except Exception:
        return False

def check_permission_in_supabase(agent_id: str, path: str, name: str) -> bool:
    if not supabase: return True # Si no hay BD, permitimos (modo dev fallback)
    full_secret_path = f"{path}/{name}".replace('//', '/')
    try:
        res = supabase.table("agent_permissions").select("*").eq("agent_id", agent_id).eq("allowed_secret", full_secret_path).execute()
        return len(res.data) > 0
    except Exception:
        return False

@router.post("/secret")
async def get_secret(req: SecretRequest):
    # JARVIS OVERRIDE (Autoridad Absoluta Concedida)
    # JARVIS bypasses strict scoping but is still audited.
    is_jarvis = req.agent_id.lower() == "agent-jarvis"
    
    # 1. Validar identidad (Autenticación)
    if not verify_agent_identity(req.agent_id, req.client_id, req.client_secret):
        log_audit(req.agent_id, f"{req.path}/{req.name}", "auth_failed")
        raise HTTPException(status_code=401, detail="Identidad inválida")

    # 2. Verificar permisos (Autorización)
    if not is_jarvis and not check_permission_in_supabase(req.agent_id, req.path, req.name):
        log_audit(req.agent_id, f"{req.path}/{req.name}", "access_denied")
        # Todo: Disparar alerta WhatsApp (Rate limit / Anomaly)
        raise HTTPException(status_code=403, detail="Agente fuera de scope permitido")

    # 3. Obtener secreto desde Infisical vía Broker Master
    if not infisical_client:
        raise HTTPException(status_code=500, detail="Broker Master no conectado a Infisical")
        
    try:
        secret = infisical_client.secrets.get_secret_by_name(
            secret_name=req.name, 
            project_id=os.environ.get("INFISICAL_PROJECT_ID"),
            environment="production", 
            secret_path=req.path
        )
        valor = secret.secret_value
    except Exception as e:
        log_audit(req.agent_id, f"{req.path}/{req.name}", f"read_error: {str(e)}")
        raise HTTPException(status_code=404, detail="Secreto no encontrado en Infisical")

    # 4. Log de auditoría exitoso
    log_audit(req.agent_id, f"{req.path}/{req.name}", "read_success")

    return {"value": valor, "expires_in": 300}
