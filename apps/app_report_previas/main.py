import os
from datetime import datetime
from apps.app_report_previas.gerador_img import gerar_img
from functions.enviar_midia_evolutionApi import enviar_midia_whatsapp


def main():
    agora = datetime.now()
    hora_minuto = agora.strftime("%H:%M")
    try:
        gerar_img()
        enviar_midia_whatsapp(
            numero= os.environ["REPORT_PHONE"],
            png_path="/app/data/relatorio_previaHxh.png",
            caption=f"Olá segue Report - {hora_minuto}"
        )
    except Exception as e:
        print(f"Erro no report: {e}")
