import os

def screenshot_erro(page, debug_path: str, etapa: str = ""):
    if not debug_path:
        return
    try:
        path = debug_path.replace(".png", f"_{etapa}.png") if etapa else debug_path
        page.screenshot(path=path, full_page=True)
        print(f"📸 Screenshot de debug salvo: {path}")
        return path  # retorna o path para quem chamou usar no envio
    except Exception as e:
        print(f"⚠️ Falha ao salvar screenshot: {e}")
        return None