def carregar_dim_tempo(conexao_postgres, df):
    """
    Carrega datas em dw.dim_tempo.

    Como a dimensão tempo é determinística e sua chave primária
    é sk_tempo, registros já existentes são ignorados.
    """

    if df.empty:
        return {
            "processados": 0
        }

    sql = """
        INSERT INTO dw.dim_tempo (
            sk_tempo,
            data_completa,
            dia,
            mes,
            nome_mes,
            trimestre,
            ano,
            dia_semana,
            nome_dia_semana,
            semana_ano,
            fim_de_semana
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )

        ON CONFLICT (sk_tempo)
        DO NOTHING
    """

    cursor = conexao_postgres.cursor()

    try:
        for _, linha in df.iterrows():
            cursor.execute(
                sql,
                (
                    int(linha["sk_tempo"]),
                    linha["data_completa"],
                    int(linha["dia"]),
                    int(linha["mes"]),
                    linha["nome_mes"],
                    int(linha["trimestre"]),
                    int(linha["ano"]),
                    int(linha["dia_semana"]),
                    linha["nome_dia_semana"],
                    int(linha["semana_ano"]),
                    bool(linha["fim_de_semana"])
                )
            )

        conexao_postgres.commit()

    except Exception:
        conexao_postgres.rollback()
        raise

    finally:
        cursor.close()

    return {
        "processados": len(df)
    }