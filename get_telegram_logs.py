import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv("C:\\AXYNTRAX\\.env")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

res = supabase.table('qwen_results').select("*").order('created_at', desc=True).limit(20).execute()
for r in reversed(res.data):
    p = r.get('payload', {})
    print(f"[{r['created_at']}] {r['order_type']}: User said: {p.get('message', '')} | JARVIS said: {p.get('response', '')}")
