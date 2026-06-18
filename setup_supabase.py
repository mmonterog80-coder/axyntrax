"""
Script de configuración de Supabase para AXYNTRAX
"""
import os
import requests
import json

print("🔧 Configurando Supabase para AXYNTRAX...")
print("=" * 50)

# Cargar variables del .env
with open('.env', 'r') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            os.environ[key] = value

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ SUPABASE_URL o SUPABASE_KEY no están en .env")
    exit(1)

print(f"✅ URL: {SUPABASE_URL}")
print(f"✅ Key: {SUPABASE_KEY[:20]}...")

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

sql_statements = [
    "CREATE TABLE IF NOT EXISTS qwen_orders (id SERIAL PRIMARY KEY, order_type VARCHAR(50) NOT NULL, payload JSONB NOT NULL, status VARCHAR(20) DEFAULT 'pending', priority INTEGER DEFAULT 1, created_at TIMESTAMP DEFAULT NOW(), processed_at TIMESTAMP, result JSONB);",
    
    "CREATE TABLE IF NOT EXISTS qwen_results (id SERIAL PRIMARY KEY, order_id INTEGER REFERENCES qwen_orders(id), result_type VARCHAR(50) NOT NULL, payload JSONB NOT NULL, status VARCHAR(20) DEFAULT 'success', created_at TIMESTAMP DEFAULT NOW(), error_message TEXT);",
    
    "CREATE INDEX IF NOT EXISTS idx_qwen_orders_status ON qwen_orders(status);",
    "CREATE INDEX IF NOT EXISTS idx_qwen_orders_priority ON qwen_orders(priority DESC);",
    "CREATE INDEX IF NOT EXISTS idx_qwen_results_order_id ON qwen_results(order_id);"
]

print("\n📊 Creando tablas...")
all_success = True

for i, sql in enumerate(sql_statements, 1):
    print(f"   [{i}/{len(sql_statements)}] {sql[:50]}...", end=" ")
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc",
            headers=headers,
            json={'query': sql}
        )
        if response.status_code in [200, 201]:
            print("✅")
        else:
            print(f"⚠️  ({response.status_code})")
            all_success = False
    except Exception as e:
        print(f"❌ {e}")
        all_success = False

print("\n" + "=" * 50)
if all_success:
    print("✅ Configuración completada")
else:
    print("⚠️  Algunas tablas requieren creación manual")
    print("\n💡 Ve a Supabase Dashboard → SQL Editor → New Query")
    print("   Pega el SQL completo desde el chat y haz clic en Run")
