from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from telemetry import router as telemetry_router
import uvicorn, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(telemetry_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "JARVIS AX Online"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# --- JARVIS PATCH: TELEGRAM WEBHOOK 404 FIX ---
from fastapi import Request
import logging, json

@app.post("/tasks/telegram/webhook")
@app.post("/telegram/webhook")
async def telegram_webhook_route(request: Request):
    logger = logging.getLogger("tg_webhook")
    try:
        data = await request.json()
        logger.info(f"TG_PAYLOAD: {json.dumps(data)}")
        
        # Enrutamiento dinámico al handler existente
        import inspect
        try:
            import telegram_handler as th
            for name, obj in inspect.getmembers(th):
                if inspect.isfunction(obj) and ('update' in name.lower() or 'telegram' in name.lower() or 'webhook' in name.lower() or 'process' in name.lower()):
                    try:
                        if inspect.iscoroutinefunction(obj):
                            await obj(data)
                        else:
                            obj(data)
                        return {"status": "ok"}
                    except Exception as e:
                        logger.warning(f"Handler {name} failed: {e}")
        except ImportError:
            logger.warning("telegram_handler module not found.")
            
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error"}
# --- END JARVIS PATCH ---
