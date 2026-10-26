from datetime import datetime

from airflow.sdk import dag, task

from etl.conexoes import (
    conectar_sql_server,
    conectar_postgres,
)

from etl.incremental.pipeline_incremental import (
    executar_dim_produto,
    executar_dim_territorio,
    executar_dim_tempo,
    executar_fato_venda,
)


@dag(
    dag_id="etl_adventureworks_dw",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["adventureworks", "etl", "dw", "incremental"],
)
def etl_adventureworks_dw():

    @task
    def carregar_dim_produto():
        sql_server = conectar_sql_server()
        postgres = conectar_postgres()

        try:
            resultado = executar_dim_produto(
                sql_server,
                postgres
            )

            print("Resultado dim_produto:")
            print(resultado)

            return resultado

        finally:
            sql_server.close()
            postgres.close()

    @task
    def carregar_dim_territorio():
        sql_server = conectar_sql_server()
        postgres = conectar_postgres()

        try:
            resultado = executar_dim_territorio(
                sql_server,
                postgres
            )

            print("Resultado dim_territorio:")
            print(resultado)

            return resultado

        finally:
            sql_server.close()
            postgres.close()

    @task
    def carregar_dim_tempo():
        sql_server = conectar_sql_server()
        postgres = conectar_postgres()

        try:
            resultado = executar_dim_tempo(
                sql_server,
                postgres
            )

            print("Resultado dim_tempo:")
            print(resultado)

            return resultado

        finally:
            sql_server.close()
            postgres.close()

    @task
    def carregar_fato_venda():
        sql_server = conectar_sql_server()
        postgres = conectar_postgres()

        try:
            resultado = executar_fato_venda(
                sql_server,
                postgres
            )

            print("Resultado fato_venda:")
            print(resultado)

            return resultado

        finally:
            sql_server.close()
            postgres.close()

    produto = carregar_dim_produto()
    territorio = carregar_dim_territorio()
    tempo = carregar_dim_tempo()

    fato = carregar_fato_venda()

    [produto, territorio, tempo] >> fato


etl_adventureworks_dw()