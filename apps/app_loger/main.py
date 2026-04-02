import pandas as pd
import json
import os
from datetime import datetime, timezone
import traceback

from apps.app_loger.extrair_loger import extrair_base_loger
from apps.app_loger.enviar_automate import enviar_para_automate
from functions.logs import log_execution
from decorators.timer import timer_log

centros = json.loads(os.environ["LOGER_CENTROS"])

@timer_log("app_loger")
def extrair(cod):
    return extrair_base_loger(cod)

@timer_log("app_loger_automate")
def enviar(df):
    enviar_para_automate(df)

def loger():
    dfs = []

    for cod, nome in centros.items():
        print(f"🔄 Processando {nome}...")
        try:
            df = extrair(cod)
            if df is not None and not df.empty:
                df['Centro'], df['Nome Centro'] = cod, nome
                dfs.append(df)
        except Exception:
            continue # Erro já logado pelo decorator

    if dfs:
        try:
            enviar(pd.concat(dfs, ignore_index=True))
        except Exception:
            pass
    else:
        print("⚠️ Sem dados para processar.")

if __name__ == '__main__':
    loger()