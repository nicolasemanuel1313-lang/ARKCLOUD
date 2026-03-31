from datetime import datetime

from apps.app_report_previas.gerador_img import gerar_img
from functions.enviar_midia_evolutionApi import enviar_midia_whatsapp

agora = datetime.now()
hora_minuto = agora.strftime("%H:%M")

if __name__ == '__main__':
    gerar_img()
    enviar_midia_whatsapp(
        numero="5531989586202",
        png_path="/app/data/relatorio_previaHxh.png",
        caption= f"Olá segue Report - {hora_minuto}"
    )
