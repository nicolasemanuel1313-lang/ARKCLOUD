import os
from datetime import datetime, timezone
import traceback

from apps.app_report_previas.gerador_img import gerar_img
from functions.enviar_midia_wpp import enviar_midia_whatsapp
from functions.logs import log_execution

# funciona local e no Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "data")
PNG_PATH = os.path.join(DATA_DIR, "relatorio_previaHxh.png")
PNG_DEBUG = os.path.join(DATA_DIR,"debug_app_report_previas.png")

def report():
    agora = datetime.now()
    hora_minuto = agora.strftime("%H:%M")
    started_at = datetime.now(timezone.utc)
    # ======================
    # Inicia
    # ======================
    try:
        gerar_img()
        enviar_midia_whatsapp(
            numero=os.environ["REPORT_PHONE"],
            png_path=PNG_PATH,
            caption=f"Olá segue Report - {hora_minuto}"
        )

    except Exception as e:
        print(f"Erro no report: {e}")
        # ======================
        # Envia mensagem com Log
        # ======================
        enviar_midia_whatsapp(
            numero=os.environ["ALERT_PHONE"],
            png_path=PNG_DEBUG,
            caption = f"Error App Report Previas - {hora_minuto} \n {e}"
        )
if __name__ == "__main__":
    report()