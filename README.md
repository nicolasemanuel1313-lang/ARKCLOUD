# ARCKCLOUD

Plataforma de automação e dados desenvolvida em Python, rodando 24/7 em VPS containerizada com Docker. 
Integra sistemas legados, fontes de dados distribuídas e relatórios em um único pipeline automatizado.

## O que faz

- Extrai dados de sistemas legados via web scraping (Playwright) em múltiplos centros de custo
- Envia os dados estruturados para o Power Automate via webhook
- Gera screenshots de relatórios do Power BI e distribui via WhatsApp automaticamente
- Alerta em tempo real com screenshot de debug quando qualquer etapa falha
- Tudo orquestrado por agendamento cron — sem intervenção manual

## Stack

- **Python 3.13** — linguagem principal
- **Playwright** — web scraping e automação de browser
- **APScheduler** — agendamento de jobs (cron)
- **Evolution API v1.8.7** — mensageria WhatsApp
- **Docker + Docker Compose** — containerização
- **VPS Hostinger** — infraestrutura (Ubuntu 24.04)

## Estrutura

ARCKCLOUD/
├── apps/
│   ├── app_loger/          # extração de dados do sistema Loger
│   └── app_report_previas/ # geração e envio de relatório Power BI
├── scheduler/              # orquestração de jobs (APScheduler)
├── functions/              # funções compartilhadas (WhatsApp, logs)
├── decorators/             # timer de performance
└── data/                   # PNGs de report e debug (volume Docker)


## Setup

**Pré-requisitos:** Docker e Docker Compose instalados.

# 1. Clone o repositório
git clone https://github.com/
cd arckcloud

# 2. Configure as variáveis de ambiente
cp .env.example .env
nano .env  # preencha com seus valores

# 3. Suba os containers
docker compose up -d

# 4. Acompanhe os logs
docker compose logs -f
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha todas as variáveis. 
Nunca versione o `.env` — ele está no `.gitignore`.

## Autor
Nicolas — Grupo Xcelis 