import pandas as pd


def extrair_dim_produto(conexao_sql_server, data_controle=None):
    """
    Extrai produtos do AdventureWorks.

    Quando data_controle é informada, retorna apenas produtos
    modificados após a última execução da ETL.
    """

    sql = """
        SELECT
            p.ProductID,
            p.Name AS NomeProduto,
            p.ProductNumber,
            p.Color,
            p.Size,
            ps.Name AS NomeSubcategoria,
            pc.Name AS NomeCategoria,
            p.ListPrice,
            p.ModifiedDate
        FROM Production.Product AS p

        LEFT JOIN Production.ProductSubcategory AS ps
            ON p.ProductSubcategoryID = ps.ProductSubcategoryID

        LEFT JOIN Production.ProductCategory AS pc
            ON ps.ProductCategoryID = pc.ProductCategoryID
    """

    parametros = None

    if data_controle is not None:
        sql += """
            WHERE p.ModifiedDate > ?
        """

        parametros = (data_controle,)

    df = pd.read_sql(
        sql,
        conexao_sql_server,
        params=parametros
    )

    return df