import os
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

# ==============================================================================
# ⚠️ ATENCIÓN: CREDENCIALES REQUERIDAS ⚠️
# ==============================================================================
# El script falló porque intentó autenticarse con "TU_ACCESS_TOKEN" (texto falso).
# Debes colocar aquí tus llaves reales de Facebook Developers.
# ==============================================================================

my_app_id = os.environ.get('FB_APP_ID', 'PON_TU_APP_ID_AQUI')
my_app_secret = os.environ.get('FB_APP_SECRET', 'PON_TU_APP_SECRET_AQUI')
my_access_token = os.environ.get('FB_ACCESS_TOKEN', 'PON_TU_ACCESS_TOKEN_AQUI')
ad_account_id = 'act_PON_TU_CUENTA_PUBLICITARIA_ID_AQUI'

def crear_campania():
    # Validar si el usuario sigue usando los valores por defecto
    if my_access_token == 'PON_TU_ACCESS_TOKEN_AQUI':
        print("❌ ERROR: No has configurado tu Access Token de Facebook.")
        print("Abre este archivo (C:\\AXYNTRAX\\scripts\\crear_campania_fb.py) y pon tus llaves reales.")
        return

    print("Iniciando conexión con Facebook Ads API...")
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

    print("Creando campaña (Método moderno V25+)...")
    account = AdAccount(ad_account_id)
    
    try:
        campaign = account.create_campaign(
            fields=[],
            params={
                Campaign.Field.name: 'Campaña AXYNTRAX Automatizada',
                Campaign.Field.status: Campaign.Status.paused,
                Campaign.Field.objective: Campaign.Objective.link_clicks,
            }
        )
        print('✅ Campaña creada exitosamente con ID: {}'.format(campaign[Campaign.Field.id]))
    except Exception as e:
        print('❌ Error de la API de Facebook:')
        print(e)

if __name__ == "__main__":
    crear_campania()
