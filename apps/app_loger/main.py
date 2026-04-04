import pandas as pd
import json
import os
import traceback
from datetime import datetime

from apps.app_loger.extrair_loger import extrair_base_loger
from apps.app_loger.enviar_automate import enviar_para_automate
from decorators.timer import timer
from functions.enviar_midia_wpp import enviar_midia_whatsapp

centros = json.loads(os.environ["LOGER_CENTROS"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "data")

@timer
def extrair(cod, debug_path):
    return extrair_base_loger(cod, debug_path=debug_path)

@timer
def enviar(df):
    enviar_para_automate(df)

def loger():
    agora = datetime.now()
    hora_minuto = agora.strftime("%d/%m %H:%M")
    dfs = []

    for cod, nome in centros.items():
        print(f"🔄 Processando {nome}...")

        # caminho do screenshot de debug para este centro
        debug_path = os.path.join(DATA_DIR, f"debug_{cod}.png")

        try:
            df = extrair(cod, debug_path)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"❌ Falha no centro {cod} - {nome}: {e}\n{tb}")

            # envia o screenshot do momento do erro se foi gerado
            if os.path.exists(debug_path):
                try:
                    enviar_midia_whatsapp(
                        numero=os.environ["ALERT_PHONE"],
                        png_path=debug_path,
                        caption=
                        f"🚨 *App Loger — Erro*\n"
                        f"📸 Debug — {cod} {nome} — {hora_minuto} \n"
                        f"❌ {str(e)}"
                    )
                except Exception:
                    pass

            raise  # interrompe — não gera df parcial

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