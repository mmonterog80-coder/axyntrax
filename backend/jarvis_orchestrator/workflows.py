"""
workflows.py — Implementación de Flujos Autónomos ("Sistema Operativo" de AXYNTRAX Corp).
"""

from plan_generator import generate_plan
from corporate import CORPORATE_STRUCTURE
import time

def execute_revenue_autopilot(product_name: str) -> dict:
    """
    Flujo 1: Revenue Autopilot
    1. PHOENIX (Marketing) genera la campaña.
    2. LEDGER (Finanzas) define el precio y ROI.
    3. SHIELD (Legal) redacta los T&C.
    """
    results = {}
    
    # Paso 1: Marketing
    print(f"[REVENUE FLOW] Llamando a PHOENIX para {product_name}...")
    phoenix_result = generate_plan(
        f"Diseña una campaña de marketing ultra-persuasiva y de 1 párrafo para vender el producto: {product_name}",
        action_type="execute",
        preferred_api=CORPORATE_STRUCTURE["PHOENIX"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["PHOENIX"]["persona"]
    )
    results["PHOENIX"] = phoenix_result
    
    # Paso 2: Finanzas
    print(f"[REVENUE FLOW] Llamando a LEDGER para {product_name}...")
    LEDGER_result = generate_plan(
        f"Basado en esta campaña: '{phoenix_result}'. Define un precio estratégico, margen de ganancia proyectado y ROI esperado (sé muy breve y numérico).",
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
    1. STARK (I+D) diseña la arquitectura.
    2. ARC (Seguridad) revisa amenazas.
    3. FORGE (Ingeniería) genera la estructura inicial de código.
    """
    results = {}
    
    # Paso 1: Diseño
    print(f"[PRODUCT FLOW] Llamando a STARK para {idea}...")
    stark_result = generate_plan(
        f"Diseña la arquitectura técnica conceptual y roadmap de este producto tecnológico: {idea} (En 3 puntos breves).",
        action_type="execute",
        preferred_api=CORPORATE_STRUCTURE["STARK"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["STARK"]["persona"]
    )
    results["STARK"] = stark_result
    
    # Paso 2: Seguridad
    print(f"[PRODUCT FLOW] Llamando a ARC para revisar arquitectura...")
    ARC_result = generate_plan(
        f"Revisa esta arquitectura: '{stark_result}'. Identifica la mayor vulnerabilidad de seguridad y cómo mitigarla. (1 párrafo estricto).",
        action_type="execute",
        preferred_api=CORPORATE_STRUCTURE["ARC"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["ARC"]["persona"]
    )
    results["ARC"] = ARC_result
    
    # Paso 3: Ingeniería
    print(f"[PRODUCT FLOW] Llamando a FORGE para iniciar código...")
    forge_result = generate_plan(
        f"Basado en la arquitectura: '{stark_result}' y la mitigación: '{ARC_result}'. Escribe un esqueleto de código Python que represente la clase principal de este sistema.",
        action_type="generate_code",
        preferred_api=CORPORATE_STRUCTURE["FORGE"]["preferred_api"],
        override_persona=CORPORATE_STRUCTURE["FORGE"]["persona"]
    )
    results["FORGE"] = forge_result
    
    return results

