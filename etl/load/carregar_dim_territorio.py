def carregar_dim_territorio(conexao_postgres, df):
    """
    Carrega territórios em dw.dim_territorio.

    Novos territórios são inseridos.
    Territórios já existentes são atualizados segundo a estratégia
    SCD Tipo 1, utilizando territory_id_oltp como chave de negócio.
    """

    if df.empty:
        return {
            "processados": 0
        }

    sql = """
        INSERT INTO dw.dim_territorio (
            territory_id_oltp,
            nome_territorio,
            codigo_pais,
            grupo_territorial
        )
        VALUES (
            %s, %s, %s, %s
        )

        ON CONFLICT (territory_id_oltp)
        DO UPDATE SET
            nome_territorio = EXCLUDED.nome_territorio,
            codigo_pais = EXCLUDED.codigo_pais,
            grupo_territorial = EXCLUDED.grupo_territorial
    """

    cursor = conexao_postgres.cursor()

    try:
        for _, linha in df.iterrows():
            cursor.execute(
                sql,
                (
                    int(linha["territory_id_oltp"]),
                    linha["nome_territorio"],
                    linha["codigo_pais"],
                    linha["grupo_territorial"]
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