import pandas as pd


def transformar_dim_tempo(df):
    """
    Transforma o calendário gerado na extração para o formato
    esperado pela dimensão dw.dim_tempo.
    """

    df = df.copy()

    # -----------------------------
    # PADRONIZAÇÃO DOS NOMES
    # -----------------------------

    df = df.rename(columns={
        "TempoKey": "sk_tempo",
        "DataCompleta": "data_completa",
        "Dia": "dia",
        "Mes": "mes",
        "NomeMes": "nome_mes",
        "Trimestre": "trimestre",
        "Ano": "ano",
        "DiaSemana": "dia_semana",
        "NomeDiaSemana": "nome_dia_semana",
        "SemanaAno": "semana_ano",
        "FimDeSemana": "fim_de_semana"
    })

    # -----------------------------
    # DATA
    # -----------------------------

    df["data_completa"] = pd.to_datetime(
        df["data_completa"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["data_completa", "sk_tempo"]
    )

    df["data_completa"] = (
        df["data_completa"]
        .dt.date
    )

    # -----------------------------
    # CAMPOS INTEIROS
    # -----------------------------

    colunas_inteiras = [
        "sk_tempo",
        "dia",
        "mes",
        "trimestre",
        "ano",
        "dia_semana",
        "semana_ano"
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
    # NOMES DOS MESES
    # -----------------------------

    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    df["nome_mes"] = (
        df["mes"]
        .map(meses)
    )

    # -----------------------------
    # NOMES DOS DIAS DA SEMANA
    # -----------------------------

    dias_semana = {
        1: "Segunda-feira",
        2: "Terça-feira",
        3: "Quarta-feira",
        4: "Quinta-feira",
        5: "Sexta-feira",
        6: "Sábado",
        7: "Domingo"
    }

    df["nome_dia_semana"] = (
        df["dia_semana"]
        .map(dias_semana)
    )

    # -----------------------------
    # FIM DE SEMANA
    # -----------------------------

    df["fim_de_semana"] = (
        df["fim_de_semana"]
        .astype(bool)
    )

    # -----------------------------
    # REMOVER DUPLICIDADES
    # -----------------------------

    df = df.drop_duplicates(
        subset=["sk_tempo"],
        keep="last"
    )

    df = df.sort_values(
        by="data_completa"
    )

    return df[
        [
            "sk_tempo",
            "data_completa",
            "dia",
            "mes",
            "nome_mes",
            "trimestre",
            "ano",
            "dia_semana",
            "nome_dia_semana",
            "semana_ano",
            "fim_de_semana"
        ]
    ]