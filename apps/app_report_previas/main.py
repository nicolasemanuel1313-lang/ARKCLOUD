import os
from datetime import datetime
from apps.app_report_previas.gerador_img import gerar_img
from functions.enviar_midia_evolutionApi import enviar_midia_whatsapp

# funciona local e no Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "data")
PNG_PATH = os.path.join(DATA_DIR, "relatorio_previaHxh.png")

def report():
    agora = datetime.now()
    hora_minuto = agora.strftime("%H:%M")
    try:
        gerar_img()
        enviar_midia_whatsapp(
            numero=os.environ["REPORT_PHONE"],
            png_path=PNG_PATH,
            caption=f"Olá segue Report - {hora_minuto}"
        )
    except Exception as e:
        print(f"Erro no report: {e}")

if __name__ == "__main__":
    report()