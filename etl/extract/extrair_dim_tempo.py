import pandas as pd


def extrair_dim_tempo(conexao_sql_server):
    """
    Gera o calendário da dimensão tempo com base no período
    existente nas vendas do AdventureWorks.
    """

    sql = """
        SELECT
            MIN(OrderDate) AS DataInicial,
            MAX(OrderDate) AS DataFinal
        FROM Sales.SalesOrderHeader
    """

    df_periodo = pd.read_sql(
        sql,
        conexao_sql_server
    )

    data_inicial = pd.to_datetime(
        df_periodo["DataInicial"].iloc[0]
    )

    data_final = pd.to_datetime(
        df_periodo["DataFinal"].iloc[0]
    )

    datas = pd.date_range(
        start=data_inicial,
        end=data_final,
        freq="D"
    )

    df = pd.DataFrame({
        "DataCompleta": datas
    })

    df["TempoKey"] = (
        df["DataCompleta"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    df["Dia"] = df["DataCompleta"].dt.day

    df["Mes"] = df["DataCompleta"].dt.month

    df["NomeMes"] = df["DataCompleta"].dt.month_name()

    df["Trimestre"] = df["DataCompleta"].dt.quarter

    df["Ano"] = df["DataCompleta"].dt.year

    df["DiaSemana"] = (
        df["DataCompleta"].dt.dayofweek + 1
    )

    df["NomeDiaSemana"] = (
        df["DataCompleta"].dt.day_name()
    )

    df["SemanaAno"] = (
        df["DataCompleta"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    df["FimDeSemana"] = (
        df["DataCompleta"]
        .dt.dayofweek
        .isin([5, 6])
    )

    return df