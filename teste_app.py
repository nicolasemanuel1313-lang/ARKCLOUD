import socket

def get_local_ip():
    # Cria um socket temporário para identificar a interface de rede ativa
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa estar conectado de verdade, o 8.8.8.8 é o DNS do Google
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
    except Exception:
        ip_local = "Não foi possível detectar"
    finally:
        s.close()
    return ip_local

print(f"Seu IP Local é: {get_local_ip()}")