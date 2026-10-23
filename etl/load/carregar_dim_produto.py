def carregar_dim_produto(conexao_postgres, df):
    """
    Carrega produtos em dw.dim_produto.

    Novos produtos são inseridos.
    Produtos já existentes são atualizados segundo a estratégia
    SCD Tipo 1, utilizando product_id_oltp como chave de negócio.
    """

    if df.empty:
        return {
            "processados": 0
        }

    sql = """
        INSERT INTO dw.dim_produto (
            product_id_oltp,
            nome_produto,
            numero_produto,
            cor,
            tamanho,
            nome_subcategoria,
            nome_categoria,
            preco_lista
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s
        )

        ON CONFLICT (product_id_oltp)
        DO UPDATE SET
            nome_produto = EXCLUDED.nome_produto,
            numero_produto = EXCLUDED.numero_produto,
            cor = EXCLUDED.cor,
            tamanho = EXCLUDED.tamanho,
            nome_subcategoria = EXCLUDED.nome_subcategoria,
            nome_categoria = EXCLUDED.nome_categoria,
            preco_lista = EXCLUDED.preco_lista
    """

    cursor = conexao_postgres.cursor()

    try:
        for _, linha in df.iterrows():
            cursor.execute(
                sql,
                (
                    int(linha["product_id_oltp"]),
                    linha["nome_produto"],
                    linha["numero_produto"],
                    linha["cor"],
                    linha["tamanho"],
                    linha["nome_subcategoria"],
                    linha["nome_categoria"],
                    float(linha["preco_lista"])
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