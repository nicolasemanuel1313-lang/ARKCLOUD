from functions.enviar_midia_evolutionApi import enviar_midia_whatsapp
from datetime import datetime


agora = datetime.now()
hora_minuto = agora.strftime("%H:%M")

enviar_midia_whatsapp(
    numero="5531989586202",
    png_path="/app/data/relatorio_previaHxh.png",
    caption= f"Olá segue Report - {hora_minuto}"
)