import pandas as pd
import json
import os
from datetime import datetime, timezone
import traceback

from apps.app_loger.extrair_loger import extrair_base_loger
from apps.app_loger.enviar_automate import enviar_para_automate
from functions.logs import log_execution
from decorators.timer import timer

centros = json.loads(os.environ["LOGER_CENTROS"])

@timer
def extrair(cod):
    return extrair_base_loger(cod)

@timer
def enviar(df):
    enviar_para_automate(df)

def loger():
    dfs = []
 
    for cod, nome in centros.items():
        print(f"🔄 Processando {nome}...")
        df = extrair(cod)
        if df is not None and not df.empty:
            df['Centro'], df['Nome Centro'] = cod, nome
            dfs.append(df)
            print(f"✅ {nome}: {len(df)} registros capturados.")
 
    # só executa se TODOS os centros foram processados com sucesso
    if dfs:
        enviar(pd.concat(dfs, ignore_index=True))
    else:
        print("⚠️ Nenhum dado capturado em nenhum centro.")
 
if __name__ == '__main__':
    loger()