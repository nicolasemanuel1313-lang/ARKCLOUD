from functions.supabase_loger import inserir_loger

def enviar_para_supabase(df):
    if df.empty:
        print("⚠️ DataFrame vazio, nada a gravar.")
        return

    # Mapeia colunas do DataFrame para colunas da tabela LOGER
    mapeamento = {
        "Transporte":           "TRANSPORTE",
        "Transportadora":       "TRANSPORTADORA",
        "Placa":                "PLACA",
        "Tipo Mercado":         "TIPO_MERCADO",
        "Data Agendamento":     "DATA_AGENDAMENTO",
        "Data Disponibilidade": "DATA_DISPONIBILIDADE",
        "Sequencia":            "SEQUENCIA",
        "Liberação Prévia":     "LIBERACAO_PREVIA",
        "Liberação Automática": "LIBERACAO_AUTOMATICA",
        "Dedicado":             "DEDICADO",
        "Centro":               "CENTRO",
        "Nome Centro":          "NOME_CENTRO",
    }

    df_mapped = df.rename(columns=mapeamento)

    # Mantém só as colunas que existem na tabela
    colunas_validas = list(mapeamento.values())
    df_mapped = df_mapped[[c for c in colunas_validas if c in df_mapped.columns]]

    # Converte para lista de dicts e trata NaN
    registros = df_mapped.fillna("").to_dict(orient="records")

    print(f"📤 Enviando {len(registros)} registros para o Supabase...")

    try:
        inserir_loger(registros)
    except Exception as e:
        print(f"❌ Erro ao gravar no Supabase: {e}")
        raise