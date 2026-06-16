import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

load_dotenv()

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")

def init_meta_api():
    if not all([META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN, META_AD_ACCOUNT_ID]):
        print("[!] Faltan credenciales de Meta Ads en las variables de entorno.")
        return False
    FacebookAdsApi.init(META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN)
    return True

def create_ad_campaign(campaign_name: str, daily_budget: int = 5000):
    """
    Crea una campaña publicitaria en estado PAUSED (Borrador) para que PHOENIX
    pueda gestionarla. daily_budget es en centavos (ej: 5000 = $50.00).
    """
    if not init_meta_api():
        return {"status": "error", "message": "API de Meta no inicializada"}
    
    try:
        account = AdAccount(f'act_{META_AD_ACCOUNT_ID}')
        
        # Parámetros básicos para crear la campaña
        params = {
            'name': campaign_name,
            'objective': 'OUTCOME_TRAFFIC', # Objetivo moderno
            'status': 'PAUSED',
            'special_ad_categories': [],
        }
        
        campaign = account.create_campaign(params=params)
        print(f"[PHOENIX] Campaña creada con éxito. ID: {campaign['id']}")
        return {"status": "success", "campaign_id": campaign['id']}
    
    except Exception as e:
        print(f"[PHOENIX] Error al crear la campaña: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Test rápido de ejecución
    res = create_ad_campaign("Campaña IA Generativa - AXYNTRAX v1")
    print(res)
