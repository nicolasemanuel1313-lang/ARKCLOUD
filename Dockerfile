FROM python:3.13-slim

# Evita prompts interativos durante instalação
ENV DEBIAN_FRONTEND=noninteractive

# Dependências do sistema necessárias para o Playwright
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia e instala dependências Python primeiro (melhor uso de cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Chromium via Playwright e todas as dependências do SO
RUN playwright install chromium --with-deps

# Copia o restante do projeto
COPY . .

# DEBUG temporário - remove depois
RUN ls -la /app

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Ponto de entrada: scheduler que orquestra tudo
CMD ["python", "-m", "scheduler.main"]