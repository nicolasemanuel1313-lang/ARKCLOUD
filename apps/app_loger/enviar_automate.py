import requests
import os

AUTOMATE_URL = os.environ["AUTOMATE_WEBHOOK_URL"]

def enviar_para_automate(df):
    if df.empty:
        print("⚠️ DataFrame vazio, nada a enviar.")
        return
    
    payload = {
        "total": len(df),
        "dados": df.to_dict(orient="records")
    }

    response = requests.post(
        AUTOMATE_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 202:
        print(f"✅ {len(df)} registros enviados para o Power Automate!")
    else:
        print(f"❌ Erro ao enviar: {response.status_code} - {response.text}")