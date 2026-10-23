import pandas as pd


def extrair_dim_territorio(conexao_sql_server, data_controle=None):
    """
    Extrai territórios de vendas do AdventureWorks.

    Quando data_controle é informada, retorna apenas territórios
    modificados após a última execução da ETL.
    """

    sql = """
        SELECT
            TerritoryID,
            Name AS NomeTerritorio,
            CountryRegionCode AS CodigoPais,
            [Group] AS GrupoTerritorial,
            ModifiedDate
        FROM Sales.SalesTerritory
    """

    parametros = None

    if data_controle is not None:
        sql += """
            WHERE ModifiedDate > ?
        """

        parametros = (data_controle,)

    df = pd.read_sql(
        sql,
        conexao_sql_server,
        params=parametros
    )

    return df