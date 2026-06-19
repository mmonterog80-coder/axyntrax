from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import httpx

router = APIRouter()

class DirectiveRequest(BaseModel):
    orden: str
    agente: str

class RetryRequest(BaseModel):
    task: str
    max_retries: int = 3

class ProgressRequest(BaseModel):
    state: Dict[str, Any]
    bot_id: str

class AcceptanceRequest(BaseModel):
    output: str
    criteria: List[str]

@router.post("/validate_directive")
async def validate_directive(req: DirectiveRequest) -> Dict:
    # Dummy Sentinel logic placeholder
    if len(req.orden) < 10:
        return {"valid": False, "correction": "Por favor provea más contexto sobre la orden."}
    return {"valid": True, "correction": ""}

@router.post("/retry_with_breaker")
async def retry_task(req: RetryRequest) -> Dict:
    # Circuit breaker mock logic
    return {"success": True, "retry": 1, "result": "Ejecución superada tras retry."}

@router.post("/send_progress")
async def send_progress_telegram(req: ProgressRequest) -> Dict:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        return {"status": "skipped", "reason": "No telegram credentials"}
        
    state = req.state
    msg = f"🚀 *AXYNTRAX Progress Report*\n"
    msg += f"📍 Skill: {state.get('current_skill', 'N/A')}\n"
    msg += f"⏱️ Retries: {state.get('retry_count', 0)}/3\n"
    msg += f"❌ Errores: {len(state.get('error_log', []))}\n"
    msg += f"✅ Checkpoints: {len(state.get('checkpoints', {}))}\n"
    
    if state.get('error_log'):
        msg += f"\n⚠️ Último error: {state.get('error_log')[-1]}\n"
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
        except Exception as e:
            print(f"Error enviando Telegram: {e}")
            
    return {"status": "sent"}

@router.post("/validate_acceptance")
async def validate_criteria(req: AcceptanceRequest) -> Dict:
    gaps = []
    for criterion in req.criteria:
        if criterion.lower() not in req.output.lower():
            gaps.append(criterion)
    return {"passed": len(gaps) == 0, "gaps": gaps}
