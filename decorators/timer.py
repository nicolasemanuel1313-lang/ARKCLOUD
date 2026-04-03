import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        duracao_ms = int((time.time() - inicio) * 1000)
        print(f"⏱ {func.__name__} — {duracao_ms}ms")
        return resultado
    return wrapper