from playwright.sync_api import sync_playwright
import time
import os
import sys 

def caminho_recurso(nome_arquivo):
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,nome_arquivo)
    return os.path.join(os.path.abspath('.'),nome_arquivo)


def gerar_img():
    user = os.environ["EMAIL_POWERBI"]
    password = os.environ["SENHA_POWERBI"]
    workspace_id = os.environ["WORKSPACE_XCELIS"]
    report_id = os.environ["RELATORIO_PREVIA_HXH"]

    url_powerbi = f"https://app.powerbi.com/groups/{workspace_id}/reports/{report_id}"

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # ======================
            # Acessar
            # ======================
            try:
                print(f"🔄 Processando - App Report Previas.")
                page.goto(url_powerbi)
                #page.get_by_role("button", name="ACEITO").click()
                page.get_by_role("textbox", name="Enter email").fill(user)
                page.get_by_role("button", name="Submit").click()
                page.get_by_role("textbox", name="Password").fill(password)
                page.get_by_role("button", name="Sign in").click()
                print(f"✅ Login realizado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de LOGIN: {e}")
                # Debug
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                folder_path = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "data")
                foto_path = os.path.join(folder_path, "debug_app_report_previas.png")
                page.screenshot(path=foto_path, full_page=True)
                raise

            page.get_by_role("button", name="No").click()
            time.sleep(20)

            # ======================
            # Gerar Img
            # ======================
            
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "data")
            foto_path = os.path.join(folder_path, "relatorio_previaHxh.png")
            try:
                page.screenshot(path=foto_path, full_page=True)
                print(f"Foto salva em: {foto_path}")
            except Exception as e:
                print(f"❌ Erro na etapa de printar Relatorio: {e}")
                # Debug
                foto_path = os.path.join(folder_path, "debug_app_report_previas.png")
                page.screenshot(path=foto_path, full_page=True)
                raise

            browser.close()
    
    except Exception as e:
                print(f"❌ Erro ao configurar Playwright: {e}")
                #Debug
                foto_path = os.path.join(folder_path, "debug_app.png")
                page.screenshot(path=foto_path, full_page=True)
                raise


        