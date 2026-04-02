import traceback
from datetime import datetime, timezone
from functools import wraps
from functions.logs import log_execution

def timer_log(app_name_prefix):
    """
    Decorator que envolve a função para:
    1. Marcar tempo de início e fim.
    2. Capturar erros silenciosamente para log.
    3. Enviar métricas para o logs.py.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            started_at = datetime.now(timezone.utc)
            
            # Tenta identificar o contexto (ex: código do centro) para o app_name
            context = f"_{args[0]}" if args else ""
            app_label = f"{app_name_prefix}{context}"
            
            try:
                result = func(*args, **kwargs)
                
                # Registro de sucesso
                log_execution(
                    app_name=app_label,
                    status="ok",
                    message="Sucesso",
                    started_at=started_at,
                    finished_at=datetime.now(timezone.utc)
                )
                return result
                
            except Exception as e:
                # Registro de erro com traceback
                log_execution(
                    app_name=app_label,
                    status="error",
                    message=str(e),
                    tb=traceback.format_exc(),
                    started_at=started_at,
                    finished_at=datetime.now(timezone.utc)
                )
                raise e # Mantém o erro vivo para o fluxo principal saber que falhou
        return wrapper
    return decorator