from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import os
import stripe
import httpx
import logging
from posthog import Posthog

router = APIRouter()

# Configuración de Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# Configuración de PostHog
posthog = Posthog(
    project_api_key=os.environ.get("POSTHOG_API_KEY", "phc_..."),
    host=os.environ.get("POSTHOG_HOST", "https://app.posthog.com")
)

# Constantes del negocio
MODULE_PRICES = {
    "veterinaria": {"price_id": "price_vet123", "mrr": 1500},
    "dental": {"price_id": "price_den123", "mrr": 1200},
    "inmobiliaria": {"price_id": "price_inm123", "mrr": 800}
}

class SaleClosedWebhook(BaseModel):
    lead_name: str
    lead_email: str
    lead_phone: str
    module_sold: str
    agent_closer: str # Ej: "Voice Pitching (sk_03)"

async def notify_telegram(message: str):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        logging.warning("Telegram credentials missing. Skipping notification.")
        return
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

@router.post("/webhook/sale-closed")
async def process_sale_closed(sale: SaleClosedWebhook):
    """
    Webhook disparado por SKILL 03 (Voice Pitching) cuando el lead acepta la propuesta.
    """
    logging.info(f"[Revenue Engine] Procesando nueva venta: {sale.module_sold} para {sale.lead_email}")
    
    if sale.module_sold not in MODULE_PRICES:
        raise HTTPException(status_code=400, detail="Módulo no reconocido.")
        
    module_info = MODULE_PRICES[sale.module_sold]
    
    try:
        # 1. Crear Cliente en Stripe
        customer = stripe.Customer.create(
            name=sale.lead_name,
            email=sale.lead_email,
            phone=sale.lead_phone,
            metadata={"module": sale.module_sold, "closer_agent": sale.agent_closer}
        )
        
        # 2. Asignar el Plan (Suscripción)
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": module_info["price_id"]}],
            payment_behavior="default_incomplete",
            payment_settings={"save_default_payment_method": "on_subscription"},
            expand=["latest_invoice.payment_intent"]
        )
        
        # 3. Registrar MRR en PostHog
        posthog.capture(
            sale.lead_email, 
            "sale_closed", 
            {
                "module": sale.module_sold,
                "mrr_added": module_info["mrr"],
                "closer_agent": sale.agent_closer,
                "stripe_customer_id": customer.id
            }
        )
        
        # 4. Notificar al CEO por Telegram
        msg = (
            f"💰 *¡NUEVA VENTA CERRADA AUTOMÁTICAMENTE!*\n\n"
            f"👤 Cliente: {sale.lead_name}\n"
            f"📦 Módulo: {sale.module_sold.capitalize()}\n"
            f"📈 MRR Añadido: S/ {module_info['mrr']}\n"
            f"🤖 Agente Cerrador: {sale.agent_closer}\n"
            f"🧾 Invoice: {subscription.latest_invoice.id if subscription.latest_invoice else 'Pendiente'}"
        )
        await notify_telegram(msg)
        
        return {
            "status": "success", 
            "customer_id": customer.id, 
            "subscription_id": subscription.id,
            "mrr_added": module_info["mrr"]
        }
        
    except Exception as e:
        logging.error(f"[Revenue Engine] Error procesando venta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
