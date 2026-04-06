from playwright.sync_api import sync_playwright
import time
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "data")
FOTO_PATH = os.path.join(DATA_DIR, "relatorio_previaHxh.png")
DEBUG_PATH = os.path.join(DATA_DIR, "debug_app_report_previas.png")

def gerar_img():
    user         = os.environ["EMAIL_POWERBI"]
    password     = os.environ["SENHA_POWERBI"]
    workspace_id = os.environ["WORKSPACE_XCELIS"]
    report_id    = os.environ["RELATORIO_PREVIA_HXH"]
    url_powerbi  = f"https://app.powerbi.com/groups/{workspace_id}/reports/{report_id}"

    def screenshot_debug(page):
        try:
            page.screenshot(path=DEBUG_PATH, full_page=True)
            print(f"📸 Screenshot de debug salvo: {DEBUG_PATH}")
        except Exception as se:
            print(f"⚠️ Falha ao salvar screenshot: {se}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page    = browser.new_context().new_page()

        try:
            print("🔄 Processando - App Report Previas.")
            page.goto(url_powerbi)
            page.get_by_role("textbox", name="Enter email").fill(user)
            page.get_by_role("button", name="Submit").click()
            page.get_by_role("textbox", name="Password").fill(password)
            page.get_by_role("button", name="Sign in").click()
            print("✅ Login realizado com sucesso.")
        except Exception as e:
            print(f"❌ Erro na etapa de LOGIN: {e}")
            screenshot_debug(page)
            raise

        page.get_by_role("button", name="No").click()
        time.sleep(20)

        try:
            page.screenshot(path=FOTO_PATH, full_page=True)
            print(f"✅ Foto salva em: {FOTO_PATH}")
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            screenshot_debug(page)
            raise
        finally:
            browser.close()

        