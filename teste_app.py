import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

# carregar .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL:", SUPABASE_URL)
print("KEY (inicio):", SUPABASE_KEY[:20] if SUPABASE_KEY else None)

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = supabase.table("LOGS").insert({
        "app_name": "teste_local",
        "status": "ok",
        "message": "teste direto da máquina",
        "started_at": datetime.now().isoformat(),
        "finished_at": datetime.now().isoformat(),
        "duration_ms": 0
    }).execute()

    print("✅ Inserido com sucesso!")
    print(response)

except Exception as e:
    print("❌ Erro:")
    print(e)