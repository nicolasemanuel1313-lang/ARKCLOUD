from functions.supabase_client import get_supabase

def inserir_loger(registros: list[dict]):
    client = get_supabase()
    response = client.table("LOGER").insert(registros).execute()
    print(f"✅ {len(response.data)} registros gravados na tabela LOGER!")
    return response