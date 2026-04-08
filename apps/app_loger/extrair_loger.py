from playwright.sync_api import sync_playwright
import pandas as pd
import os


def extrair_base_loger(nomeCentro, debug_path=None):
    url = os.environ["URL_LOGER"]
    user = os.environ["LOGER_USER"]
    password = os.environ["LOGER_PASSWORD"]

    def screenshot_erro(page, etapa):
        if debug_path:
            try:
                page.screenshot(path=debug_path, full_page=True)
                print(f"📸 Screenshot de debug salvo: {debug_path}")
            except Exception as se:
                print(f"⚠️ Falha ao salvar screenshot: {se}")

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # ======================
            # LOGIN
            # ======================
            try:
                page.goto(url)
                page.get_by_role("button", name="ACEITO").click()
                page.get_by_role("textbox", name="Usuário").fill(user)
                page.get_by_role("textbox", name="Senha").fill(password)
                page.get_by_role("button", name="Entrar").click()
                page.wait_for_load_state("networkidle")
                print(f"✅ Login realizado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de LOGIN: {e}")
                screenshot_erro(page, "LOGIN")
                raise

            # ======================
            # SELEÇÃO DO CENTRO
            # ======================
            try:
                page.get_by_role("textbox", name="Buscar por centro").fill(nomeCentro)
                page.get_by_role("button", name=" Pesquisar").click()
                page.get_by_role("gridcell", name=nomeCentro).first.dblclick()
                # Aguarda o botão aparecer antes de clicar (substitui sleep(5))
                agendamento_btn = page.get_by_role("button", name="Agendamento De Carga")
                agendamento_btn.wait_for(state="visible", timeout=15000)
                agendamento_btn.click()
                page.get_by_role("textbox", name="Acesso rápido").fill('29')
                page.get_by_role("button", name="search").click()
                print(f"✅ Centro {nomeCentro} selecionado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de SELEÇÃO DO CENTRO {nomeCentro}: {e}")
                screenshot_erro(page, "SELECAO_CENTRO")
                raise

            # ======================
            # LOCALIZAR FRAME CORRETO
            # ======================
            try:
                frame_alvo = None
                timeout_ms = 30000
                interval_ms = 500
                elapsed = 0

                while elapsed < timeout_ms:
                    for f in page.frames:
                        if "LOGER_WEB/consultaFilaTransporteDisponibilidadeImediata" in f.url and not f.is_detached():
                            if f.locator('#btnConsultar').count() > 0:
                                frame_alvo = f
                                break
                    if frame_alvo:
                        break
                    page.wait_for_timeout(interval_ms)
                    elapsed += interval_ms

                if not frame_alvo:
                    raise Exception("Frame não encontrado após 30 segundos!")

                print(f"✅ Frame localizado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de LOCALIZAR FRAME: {e}")
                screenshot_erro(page, "LOCALIZAR_FRAME")
                raise

            # ======================
            # CLICAR EM CONSULTAR
            # ======================
            try:
                frame_alvo.wait_for_selector('.loader-container', state='hidden', timeout=30000)
                frame_alvo.locator('#btnConsultar').click()
                print(f"✅ Botão Consultar clicado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de CLICAR EM CONSULTAR: {e}")
                screenshot_erro(page, "CLICAR_CONSULTAR")
                raise

            # ======================
            # CAPTURAR TRANSPORTES
            # ======================
            print("Aguardando resultados...")
            try:
                # Timeout maior pois substitui o sleep(30) que havia antes
                frame_alvo.wait_for_selector('.loader-container', state='hidden', timeout=60000)
            except Exception as e:
                print(f"❌ Erro aguardando loader sumir após consulta: {e}")
                screenshot_erro(page, "LOADER")
                raise

            try:
                frame_alvo.wait_for_selector(
                    '#filaTransporteDisponibilidadeImediataGrid tr.jqgrow',
                    timeout=15000
                )
            except Exception:
                print(f"⚠️ Centro {nomeCentro}: tabela vazia, nenhum transporte na fila.")
                browser.close()
                return pd.DataFrame()

            try:
                dados = frame_alvo.evaluate("""
                    () => {
                        const linhas = document.querySelectorAll('#filaTransporteDisponibilidadeImediataGrid tr.jqgrow');
                        const resultado = [];

                        linhas.forEach(linha => {
                            const get = (col) => {
                                const td = linha.querySelector(`td[aria-describedby="filaTransporteDisponibilidadeImediataGrid_${col}"]`);
                                return td ? td.getAttribute('title') : '';
                            };

                            resultado.push({
                                'Transporte':           get('transporte'),
                                'Transportadora':       get('transportadora'),
                                'Placa':                get('placa'),
                                'Tipo Mercado':         get('tipoMercado'),
                                'Data Agendamento':     get('dataAgendamento'),
                                'Data Disponibilidade': get('dataDisponibilidade'),
                                'Sequencia':            get('sequencia'),
                                'Liberação Prévia':     get('liberacaoPrevia'),
                                'Liberação Automática': get('liberacaoAutomatica'),
                                'Dedicado':             get('dedicado'),
                            });
                        });

                        return resultado;
                    }
                """)

                df = pd.DataFrame(dados)
                print(f"✅ {len(df)} registros capturados!")
                browser.close()
                return df

            except Exception as e:
                print(f"❌ Erro na etapa de CAPTURAR DADOS DA TABELA: {e}")
                screenshot_erro(page, "CAPTURAR_DADOS")
                raise

    except Exception as e:
        print(f"❌ Erro geral no centro {nomeCentro}: {e}")
        raise
