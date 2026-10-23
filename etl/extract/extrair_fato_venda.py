import pandas as pd


def extrair_fato_venda(conexao_sql_server, data_controle=None):
    """
    Extrai vendas do AdventureWorks.

    Quando data_controle é informada, retorna apenas registros
    novos ou modificados após a última execução da ETL.

    O custo unitário utiliza prioritariamente o histórico de custos.
    Caso não exista um custo histórico válido para a data da venda,
    é utilizado o StandardCost atual do produto como fallback.
    """

    sql = """
        SELECT
            soh.OrderDate,

            sod.ProductID,
            soh.TerritoryID,

            sod.SalesOrderID,
            sod.SalesOrderDetailID,

            sod.OrderQty,
            sod.UnitPrice,
            sod.UnitPriceDiscount,

            sod.OrderQty * sod.UnitPrice
                AS ValorBrutoItem,

            sod.OrderQty
                * sod.UnitPrice
                * sod.UnitPriceDiscount
                AS ValorDesconto,

            sod.LineTotal
                AS ValorReceita,

            COALESCE(
                custo_historico.StandardCost,
                p.StandardCost
            ) AS CustoUnitarioAplicado,

            CASE
                WHEN custo_historico.StandardCost IS NOT NULL
                    THEN 'HISTORICO'
                ELSE 'FALLBACK_ATUAL'
            END AS OrigemCusto,

            sod.OrderQty * COALESCE(
                custo_historico.StandardCost,
                p.StandardCost
            ) AS CustoTotal,

            CASE
                WHEN soh.ModifiedDate > sod.ModifiedDate
                    THEN soh.ModifiedDate
                ELSE sod.ModifiedDate
            END AS ModifiedDate

        FROM Sales.SalesOrderDetail AS sod

        INNER JOIN Sales.SalesOrderHeader AS soh
            ON sod.SalesOrderID = soh.SalesOrderID

        INNER JOIN Production.Product AS p
            ON sod.ProductID = p.ProductID

        OUTER APPLY
        (
            SELECT TOP 1
                pch.StandardCost
            FROM Production.ProductCostHistory AS pch
            WHERE pch.ProductID = sod.ProductID
              AND pch.StartDate <= soh.OrderDate
              AND (
                    pch.EndDate IS NULL
                    OR pch.EndDate >= soh.OrderDate
                  )
            ORDER BY pch.StartDate DESC
        ) AS custo_historico
    """

    parametros = None

    if data_controle is not None:
        sql += """
            WHERE
                CASE
                    WHEN soh.ModifiedDate > sod.ModifiedDate
                        THEN soh.ModifiedDate
                    ELSE sod.ModifiedDate
                END > ?
        """

        parametros = (data_controle,)

    df = pd.read_sql(
        sql,
        conexao_sql_server,
        params=parametros
    )

    return df