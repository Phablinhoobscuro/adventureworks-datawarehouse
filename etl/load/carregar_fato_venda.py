import pandas as pd


def carregar_fato_venda(conexao_postgres, df):
    """
    Carrega registros em dw.fato_venda.

    A combinação sales_order_id + sales_order_detail_id representa
    o grão da tabela fato.

    Registros novos são inseridos.
    Registros já existentes são atualizados, garantindo uma
    carga incremental idempotente e sem duplicidades.
    """

    if df.empty:
        return {
            "processados": 0
        }

    sql = """
        INSERT INTO dw.fato_venda (
            sales_order_id,
            sales_order_detail_id,
            sk_tempo,
            sk_produto,
            sk_territorio,
            quantidade,
            preco_unitario,
            percentual_desconto_item,
            valor_receita,
            valor_bruto_item,
            valor_desconto,
            custo_unitario_aplicado,
            origem_custo,
            custo_total,
            margem_bruta
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )

        ON CONFLICT (
            sales_order_id,
            sales_order_detail_id
        )
        DO UPDATE SET
            sk_tempo = EXCLUDED.sk_tempo,
            sk_produto = EXCLUDED.sk_produto,
            sk_territorio = EXCLUDED.sk_territorio,
            quantidade = EXCLUDED.quantidade,
            preco_unitario = EXCLUDED.preco_unitario,
            percentual_desconto_item =
                EXCLUDED.percentual_desconto_item,
            valor_receita = EXCLUDED.valor_receita,
            valor_bruto_item = EXCLUDED.valor_bruto_item,
            valor_desconto = EXCLUDED.valor_desconto,
            custo_unitario_aplicado =
                EXCLUDED.custo_unitario_aplicado,
            origem_custo = EXCLUDED.origem_custo,
            custo_total = EXCLUDED.custo_total,
            margem_bruta = EXCLUDED.margem_bruta
    """

    cursor = conexao_postgres.cursor()

    try:
        for _, linha in df.iterrows():

            custo_unitario = (
                None
                if pd.isna(linha["custo_unitario_aplicado"])
                else float(linha["custo_unitario_aplicado"])
            )

            custo_total = (
                None
                if pd.isna(linha["custo_total"])
                else float(linha["custo_total"])
            )

            margem_bruta = (
                None
                if pd.isna(linha["margem_bruta"])
                else float(linha["margem_bruta"])
            )

            cursor.execute(
                sql,
                (
                    int(linha["sales_order_id"]),
                    int(linha["sales_order_detail_id"]),
                    int(linha["sk_tempo"]),
                    int(linha["sk_produto"]),
                    int(linha["sk_territorio"]),
                    int(linha["quantidade"]),
                    float(linha["preco_unitario"]),
                    float(linha["percentual_desconto_item"]),
                    float(linha["valor_receita"]),
                    float(linha["valor_bruto_item"]),
                    float(linha["valor_desconto"]),
                    custo_unitario,
                    linha["origem_custo"],
                    custo_total,
                    margem_bruta
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