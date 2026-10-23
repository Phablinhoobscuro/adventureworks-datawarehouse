import pandas as pd


def buscar_chaves_dimensoes(conexao_postgres):
    """
    Busca as chaves substitutas e as respectivas chaves de negócio
    das dimensões necessárias para a transformação da fato_venda.

    Retorna:
        df_produto
        df_territorio
    """

    cursor = conexao_postgres.cursor()

    try:
        # -----------------------------
        # DIM_PRODUTO
        # -----------------------------

        cursor.execute(
            """
            SELECT
                sk_produto,
                product_id_oltp
            FROM dw.dim_produto
            """
        )

        produtos = cursor.fetchall()

        df_produto = pd.DataFrame(
            produtos,
            columns=[
                "sk_produto",
                "product_id_oltp"
            ]
        )

        # -----------------------------
        # DIM_TERRITORIO
        # -----------------------------

        cursor.execute(
            """
            SELECT
                sk_territorio,
                territory_id_oltp
            FROM dw.dim_territorio
            """
        )

        territorios = cursor.fetchall()

        df_territorio = pd.DataFrame(
            territorios,
            columns=[
                "sk_territorio",
                "territory_id_oltp"
            ]
        )

    finally:
        cursor.close()

    return (
        df_produto,
        df_territorio
    )