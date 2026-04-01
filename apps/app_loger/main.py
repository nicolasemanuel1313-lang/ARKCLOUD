import pandas as pd
import json
import os
from datetime import datetime, timezone
import traceback

from apps.app_loger.extrair_loger import extrair_base_loger
from apps.app_loger.enviar_automate import enviar_para_automate
from functions.logs import log_execution

centros = json.loads(os.environ["LOGER_CENTROS"])

def loger():
    dfs = []

    for cod, nome in centros.items():
        print(f"\n{'='*50}")
        print(f"🔄 Extraindo centro: {cod} - {nome}")
        print(f"{'='*50}")
        # ======================
        # Inicia
        # ======================
        try:
            started_at = datetime.now(timezone.utc)
            df = extrair_base_loger(cod)
            if not df.empty:
                df['Centro'] = cod
                df['Nome Centro'] = nome
                dfs.append(df)
                print(f"✅ {cod} - {nome}: {len(df)} registros capturados!")
                # ======================
                # Grava Log
                # ======================
                log_execution(f"app_loger_{nome}", "ok", "Executado com sucesso", started_at=started_at, finished_at=datetime.now(timezone.utc))
        except Exception as e:
            print(f"❌ Erro no centro {cod} - {nome}: {e}")
            # ======================
            # Grava Log
            # ======================
            log_execution(f"app_loger_{nome}", "error", str(e), tb=traceback.format_exc(), started_at=started_at, finished_at=datetime.now(timezone.utc))
    
    # ======================
    # Envia resultado para power automate.
    # ======================
    try:
        started_at = datetime.now(timezone.utc)
        if dfs:
            df_final = pd.concat(dfs, ignore_index=True)
            enviar_para_automate(df_final)
            # ======================
            # Grava Log
            # ======================
            log_execution("app_loger_automate", "ok", "Executado com sucesso", started_at=started_at, finished_at=datetime.now(timezone.utc))
        else:
            print("\n⚠️ Nenhum dado capturado em nenhum centro!")
            log_execution("app_loger_automate", "ok", "Executado com sucesso/Df Vazio", started_at=started_at, finished_at=datetime.now(timezone.utc))
        
    except Exception as e:
        # ======================
        # Grava Log
        # ======================
        log_execution("app_loger_automate", "error", str(e), tb=traceback.format_exc(), started_at=started_at, finished_at=datetime.now(timezone.utc))

if __name__ == '__main__':
    loger()