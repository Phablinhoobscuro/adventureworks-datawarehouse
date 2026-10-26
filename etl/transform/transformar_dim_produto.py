import pandas as pd


def transformar_dim_produto(df):
    """
    Transforma os dados de produtos extraídos do AdventureWorks
    para o formato esperado pela dimensão dw.dim_produto.
    """

    df = df.copy()

    df = df.rename(columns={
        "ProductID": "product_id_oltp",
        "NomeProduto": "nome_produto",
        "ProductNumber": "numero_produto",
        "Color": "cor",
        "Size": "tamanho",
        "NomeSubcategoria": "nome_subcategoria",
        "NomeCategoria": "nome_categoria",
        "ListPrice": "preco_lista",
        "ModifiedDate": "modified_date"
    })

    # -----------------------------
    # CHAVE DE NEGÓCIO
    # -----------------------------

    df["product_id_oltp"] = pd.to_numeric(
        df["product_id_oltp"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["product_id_oltp"]
    )

    df["product_id_oltp"] = (
        df["product_id_oltp"]
        .astype(int)
    )

    # -----------------------------
    # ATRIBUTOS TEXTUAIS
    # -----------------------------

    df["nome_produto"] = (
        df["nome_produto"]
        .fillna("Não informado")
    )

    df["numero_produto"] = (
        df["numero_produto"]
        .fillna("Não informado")
    )

    df["cor"] = (
        df["cor"]
        .fillna("Não informado")
    )

    df["tamanho"] = (
        df["tamanho"]
        .fillna("N/A")
    )

    df["nome_subcategoria"] = (
        df["nome_subcategoria"]
        .fillna("Não classificado")
    )

    df["nome_categoria"] = (
        df["nome_categoria"]
        .fillna("Não classificado")
    )

    # -----------------------------
    # PREÇO
    # -----------------------------

    df["preco_lista"] = pd.to_numeric(
        df["preco_lista"],
        errors="coerce"
    ).fillna(0)

    # -----------------------------
    # DATA DE ALTERAÇÃO DA ORIGEM
    # -----------------------------

    df["modified_date"] = pd.to_datetime(
        df["modified_date"],
        errors="coerce"
    )

    # -----------------------------
    # REMOVER DUPLICIDADES
    # -----------------------------

    df = df.drop_duplicates(
        subset=["product_id_oltp"],
        keep="last"
    )

    return df[
        [
            "product_id_oltp",
            "nome_produto",
            "numero_produto",
            "cor",
            "tamanho",
            "nome_subcategoria",
            "nome_categoria",
            "preco_lista",
            "modified_date"
        ]
    ]