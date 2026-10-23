import pandas as pd


def transformar_fato_venda(
    df_vendas,
    df_produto,
    df_territorio
):
    """
    Transforma os dados de vendas extraídos do AdventureWorks
    para o formato esperado pela fato dw.fato_venda.

    As chaves substitutas de produto e território são obtidas
    a partir das dimensões já carregadas no Data Warehouse.
    """

    df = df_vendas.copy()

    df_produto = df_produto.copy()
    df_territorio = df_territorio.copy()

    # -----------------------------
    # PADRONIZAÇÃO DOS NOMES
    # -----------------------------

    df = df.rename(columns={
        "SalesOrderID": "sales_order_id",
        "SalesOrderDetailID": "sales_order_detail_id",
        "OrderQty": "quantidade",
        "UnitPrice": "preco_unitario",
        "UnitPriceDiscount": "percentual_desconto_item",
        "ValorReceita": "valor_receita",
        "ValorBrutoItem": "valor_bruto_item",
        "ValorDesconto": "valor_desconto",
        "CustoUnitarioAplicado": "custo_unitario_aplicado",
        "OrigemCusto": "origem_custo",
        "CustoTotal": "custo_total",
        "ModifiedDate": "modified_date"
    })

    # -----------------------------
    # DATA / SK_TEMPO
    # -----------------------------

    df["OrderDate"] = pd.to_datetime(
        df["OrderDate"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["OrderDate"]
    )

    df["sk_tempo"] = (
        df["OrderDate"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    # -----------------------------
    # IDS DA ORIGEM
    # -----------------------------

    df["ProductID"] = pd.to_numeric(
        df["ProductID"],
        errors="coerce"
    ).astype("Int64")

    df["TerritoryID"] = pd.to_numeric(
        df["TerritoryID"],
        errors="coerce"
    ).astype("Int64")

    df_produto["product_id_oltp"] = pd.to_numeric(
        df_produto["product_id_oltp"],
        errors="coerce"
    ).astype("Int64")

    df_territorio["territory_id_oltp"] = pd.to_numeric(
        df_territorio["territory_id_oltp"],
        errors="coerce"
    ).astype("Int64")

    # -----------------------------
    # SK_PRODUTO
    # -----------------------------

    df = df.merge(
        df_produto[
            [
                "sk_produto",
                "product_id_oltp"
            ]
        ],
        left_on="ProductID",
        right_on="product_id_oltp",
        how="left"
    )

    # Produto desconhecido
    df["sk_produto"] = (
        df["sk_produto"]
        .fillna(-1)
        .astype(int)
    )

    # -----------------------------
    # SK_TERRITORIO
    # -----------------------------

    df = df.merge(
        df_territorio[
            [
                "sk_territorio",
                "territory_id_oltp"
            ]
        ],
        left_on="TerritoryID",
        right_on="territory_id_oltp",
        how="left"
    )

    # Território desconhecido
    df["sk_territorio"] = (
        df["sk_territorio"]
        .fillna(-1)
        .astype(int)
    )

    # -----------------------------
    # CAMPOS INTEIROS
    # -----------------------------

    colunas_inteiras = [
        "sales_order_id",
        "sales_order_detail_id",
        "quantidade"
    ]

    for coluna in colunas_inteiras:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    df = df.dropna(
        subset=colunas_inteiras
    )

    for coluna in colunas_inteiras:
        df[coluna] = (
            df[coluna]
            .astype(int)
        )

    # -----------------------------
    # CAMPOS NUMÉRICOS
    # -----------------------------

    colunas_numericas = [
        "preco_unitario",
        "percentual_desconto_item",
        "valor_receita",
        "valor_bruto_item",
        "valor_desconto",
        "custo_unitario_aplicado",
        "custo_total"
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # -----------------------------
    # ORIGEM DO CUSTO
    # -----------------------------

    df["origem_custo"] = (
        df["origem_custo"]
        .fillna("FALLBACK_ATUAL")
    )

    # -----------------------------
    # MARGEM BRUTA
    # -----------------------------

    df["margem_bruta"] = (
        df["valor_receita"]
        - df["custo_total"]
    )

    # -----------------------------
    # CONTROLE INCREMENTAL
    # -----------------------------

    df["modified_date"] = pd.to_datetime(
        df["modified_date"],
        errors="coerce"
    )

    # -----------------------------
    # REMOVER DUPLICIDADES
    # -----------------------------

    df = df.drop_duplicates(
        subset=[
            "sales_order_id",
            "sales_order_detail_id"
        ],
        keep="last"
    )

    return df[
        [
            "sales_order_id",
            "sales_order_detail_id",
            "sk_tempo",
            "sk_produto",
            "sk_territorio",
            "quantidade",
            "preco_unitario",
            "percentual_desconto_item",
            "valor_receita",
            "valor_bruto_item",
            "valor_desconto",
            "custo_unitario_aplicado",
            "origem_custo",
            "custo_total",
            "margem_bruta",
            "modified_date"
        ]
    ]