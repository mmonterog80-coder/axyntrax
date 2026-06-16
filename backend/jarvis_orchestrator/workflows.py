"""
workflows.py â€” ImplementaciÃ³n de Flujos AutÃ³nomos ("Sistema Operativo" de AXYNTRAX Corp).
"""

from plan_generator import generate_plan
from corporate import CORPORATE_STRUCTURE
import time

def execute_revenue_autopilot(product_name: str) -> dict:
    """
    Flujo 1: Revenue Autopilot
    1. PHOENIX (Marketing) genera la campaÃ±a.
    2. LEDGER (Finanzas) define el precio y ROI.
    3. SHIELD (Legal) redacta los T&C.
    """
    results = {}
    
    # Paso 1: Marketing
    print(f"[REVENUE FLOW] Llamando a PHOENIX para {product_name}...")
    phoenix_result = generate_plan(
        f"DiseÃ±a una campaÃ±a de marketing ultra-persuasiva y de 1 pÃ¡rrafo para vender el producto: {product_name}",
        action_type="execute",
        preferred_api=CORPORATE_STRUCTURE["PHOENIX"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["PHOENIX"]["persona"]
    )
    results["PHOENIX"] = phoenix_result
    
    # Paso 2: Finanzas
    print(f"[REVENUE FLOW] Llamando a LEDGER para {product_name}...")
    LEDGER_result = generate_plan(
        f"Basado en esta campaÃ±a: '{phoenix_result}'. Define un precio estratÃ©gico, margen de ganancia proyectado y ROI esperado (sÃ© muy breve y numÃ©rico).",
        action_type="execute",
        preferred_api=CORPORATE_STRUCTURE["LEDGER"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["LEDGER"]["persona"]
    )
    results["LEDGER"] = LEDGER_result
    
    # Paso 3: Legal
    print(f"[REVENUE FLOW] Llamando a SHIELD para {product_name}...")
    shield_result = generate_plan(
        f"Redacta un aviso legal estricto de 2 oraciones para proteger a la empresa sobre la venta de este producto con precio: {LEDGER_result}",
        action_type="execute",
        preferred_api=CORPORATE_STRUCTURE["SHIELD"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["SHIELD"]["persona"]
    )
    results["SHIELD"] = shield_result
    
    return results

def execute_product_pipeline(idea: str) -> dict:
    """
    Flujo 2: Product Pipeline
    1. STARK (I+D) diseÃ±a la arquitectura.
    2. ARC (Seguridad) revisa amenazas.
    3. FORGE (IngenierÃ­a) genera la estructura inicial de cÃ³digo.
    """
    results = {}
    
    # Paso 1: DiseÃ±o
    print(f"[PRODUCT FLOW] Llamando a STARK para {idea}...")
    stark_result = generate_plan(
        f"DiseÃ±a la arquitectura tÃ©cnica conceptual y roadmap de este producto tecnolÃ³gico: {idea} (En 3 puntos breves).",
        action_type="execute",
        preferred_api=CORPORATE_STRUCTURE["STARK"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["STARK"]["persona"]
    )
    results["STARK"] = stark_result
    
    # Paso 2: Seguridad
    print(f"[PRODUCT FLOW] Llamando a ARC para revisar arquitectura...")
    ARC_result = generate_plan(
        f"Revisa esta arquitectura: '{stark_result}'. Identifica la mayor vulnerabilidad de seguridad y cÃ³mo mitigarla. (1 pÃ¡rrafo estricto).",
        action_type="execute",
        preferred_api=CORPORATE_STRUCTURE["ARC"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["ARC"]["persona"]
    )
    results["ARC"] = ARC_result
    
    # Paso 3: IngenierÃ­a
    print(f"[PRODUCT FLOW] Llamando a FORGE para iniciar cÃ³digo...")
    forge_result = generate_plan(
        f"Basado en la arquitectura: '{stark_result}' y la mitigaciÃ³n: '{ARC_result}'. Escribe un esqueleto de cÃ³digo Python que represente la clase principal de este sistema.",
        action_type="generate_code",
        preferred_api=CORPORATE_STRUCTURE["FORGE"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["FORGE"]["persona"]
    )
    results["FORGE"] = forge_result
    
    return results

