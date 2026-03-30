import pandas as pd
import json
import os

from apps.app_loger.extrair_loger import extrair_base_loger
from apps.app_loger.enviar_automate import enviar_para_automate
from apps.app_loger.enviar_supabase import enviar_para_supabase


centros = json.loads(os.environ["LOGER_CENTROS"])

def loger():
    dfs = []

    for cod, nome in centros.items():
        print(f"\n{'='*50}")
        print(f"🔄 Extraindo centro: {cod} - {nome}")
        print(f"{'='*50}")
        try:
            df = extrair_base_loger(cod)
            if not df.empty:
                df['Centro'] = cod
                df['Nome Centro'] = nome
                dfs.append(df)
                print(f"✅ {cod} - {nome}: {len(df)} registros capturados!")
        except Exception as e:
            print(f"❌ Erro no centro {cod} - {nome}: {e}")

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        #enviar_para_supabase(df_final)
        enviar_para_automate(df_final)
    else:
        print("\n⚠️ Nenhum dado capturado em nenhum centro!")

if __name__ == '__main__':
    loger()