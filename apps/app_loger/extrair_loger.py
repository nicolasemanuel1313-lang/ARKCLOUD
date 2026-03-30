from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os


def extrair_base_loger(nomeCentro):
    url = os.environ["URL_LOGER"]
    user = os.environ["LOGER_USER"]
    password = os.environ["LOGER_PASSWORD"]

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
                print(f"✅ Login realizado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de LOGIN: {e}")
                raise

            # ======================
            # SELEÇÃO DO CENTRO
            # ======================
            try:
                page.get_by_role("textbox", name="Buscar por centro").fill(nomeCentro)
                page.get_by_role("button", name=" Pesquisar").click()
                page.get_by_role("gridcell", name=nomeCentro).first.dblclick()
                page.get_by_role("button", name="Agendamento De Carga").click()
                page.get_by_role("textbox", name="Acesso rápido").fill('29')
                page.get_by_role("button", name="search").click()
                print(f"✅ Centro {nomeCentro} selecionado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de SELEÇÃO DO CENTRO {nomeCentro}: {e}")
    
                # debug e print
                page.wait_for_load_state("networkidle")
                page.screenshot(path=f"/app/data/screenshot_{nomeCentro}.png")

                raise

            # ======================
            # LOCALIZAR FRAME CORRETO
            # ======================
            try:
                frame_alvo = None
                for _ in range(60):
                    for f in page.frames:
                        if "LOGER_WEB/consultaFilaTransporteDisponibilidadeImediata" in f.url and not f.is_detached():
                            if f.locator('#btnConsultar').count() > 0:
                                frame_alvo = f
                                break
                    if frame_alvo:
                        break
                    time.sleep(0.5)

                if not frame_alvo:
                    raise Exception("Frame não encontrado após 30 segundos!")

                print(f"✅ Frame localizado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de LOCALIZAR FRAME: {e}")
                raise

            # ======================
            # CLICAR EM CONSULTAR
            # ======================
            try:
                frame_alvo.wait_for_selector('.loader-container', state='hidden', timeout=30000)
                frame_alvo.evaluate("document.querySelector('#btnConsultar').click()")
                print(f"✅ Botão Consultar clicado com sucesso.")
            except Exception as e:
                print(f"❌ Erro na etapa de CLICAR EM CONSULTAR: {e}")
                raise

            # ======================
            # CAPTURAR TRANSPORTES
            # ======================
            print("Aguardando resultados...")
            try:
                frame_alvo.wait_for_selector('.loader-container', state='hidden', timeout=30000)
            except Exception as e:
                print(f"❌ Erro aguardando loader sumir após consulta: {e}")
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
                raise

    except Exception as e:
        print(f"❌ Erro geral no centro {nomeCentro}: {e}")
        raise