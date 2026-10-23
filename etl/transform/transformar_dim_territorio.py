import pandas as pd


def transformar_dim_territorio(df):
    """
    Transforma os dados de territórios extraídos do AdventureWorks
    para o formato esperado pela dimensão dw.dim_territorio.
    """

    df = df.copy()

    df = df.rename(columns={
        "TerritoryID": "territory_id_oltp",
        "NomeTerritorio": "nome_territorio",
        "CodigoPais": "codigo_pais",
        "GrupoTerritorial": "grupo_territorial",
        "ModifiedDate": "modified_date"
    })

    # -----------------------------
    # CHAVE DE NEGÓCIO
    # -----------------------------

    df["territory_id_oltp"] = pd.to_numeric(
        df["territory_id_oltp"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["territory_id_oltp"]
    )

    df["territory_id_oltp"] = (
        df["territory_id_oltp"]
        .astype(int)
    )

    # -----------------------------
    # ATRIBUTOS TEXTUAIS
    # -----------------------------

    df["nome_territorio"] = (
        df["nome_territorio"]
        .fillna("Não informado")
    )

    df["codigo_pais"] = (
        df["codigo_pais"]
        .fillna("Não informado")
    )

    df["grupo_territorial"] = (
        df["grupo_territorial"]
        .fillna("Não informado")
    )

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
        subset=["territory_id_oltp"],
        keep="last"
    )

    return df[
        [
            "territory_id_oltp",
            "nome_territorio",
            "codigo_pais",
            "grupo_territorial",
            "modified_date"
        ]
    ]