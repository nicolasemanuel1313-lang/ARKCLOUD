import requests
import base64
import os

EVOLUTION_URL = os.environ["EVOLUTION_URL"]
EVOLUTION_APIKEY = os.environ["EVOLUTION_APIKEY"]
EVOLUTION_INSTANCE = os.environ["EVOLUTION_INSTANCE"]

def enviar_midia_whatsapp(numero: str, png_path: str, caption: str = "Segue Report"):
    with open(png_path, "rb") as image_file:
        media_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    file_name = os.path.basename(png_path)

    payload = {
        "number": numero,
        "mediaMessage": {
            "mediatype": "image",
            "mimetype": "image/png",
            "caption": caption,
            "media": media_base64,
            "fileName": file_name
        }
    }

    headers = {
        "apikey": EVOLUTION_APIKEY,
        "Content-Type": "application/json"
    }

    url = f"{EVOLUTION_URL}/message/sendMedia/{EVOLUTION_INSTANCE}"

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"✅ Mídia enviada para {numero} — {file_name}")
        return response.json()
    except Exception as e:
        print(f"❌ Erro ao enviar mídia para {numero}: {e}")
        raise