[1mdiff --git a/dags/etl_adventureworks_dw.py b/dags/etl_adventureworks_dw.py[m
[1mindex c835746..2da6cca 100644[m
[1m--- a/dags/etl_adventureworks_dw.py[m
[1m+++ b/dags/etl_adventureworks_dw.py[m
[36m@@ -1,4 +1,4 @@[m
[31m-from datetime import datetime[m
[32m+[m[32mfrom datetime import datetime, timedelta[m
 [m
 from airflow.sdk import dag, task[m
 [m
[36m@@ -17,13 +17,62 @@[m [mfrom etl.incremental.pipeline_incremental import ([m
 [m
 @dag([m
     dag_id="etl_adventureworks_dw",[m
[32m+[m[32m    description=([m
[32m+[m[32m        "ETL incremental do AdventureWorks2016 "[m
[32m+[m[32m        "para o Data Warehouse PostgreSQL."[m
[32m+[m[32m    ),[m
     schedule=None,[m
     start_date=datetime(2026, 1, 1),[m
     catchup=False,[m
[31m-    tags=["adventureworks", "etl", "dw", "incremental"],[m
[32m+[m[32m    max_active_runs=1,[m
[32m+[m[32m    default_args={[m
[32m+[m[32m        "retries": 2,[m
[32m+[m[32m        "retry_delay": timedelta(minutes=1),[m
[32m+[m[32m    },[m
[32m+[m[32m    tags=[[m
[32m+[m[32m        "adventureworks",[m
[32m+[m[32m        "etl",[m
[32m+[m[32m        "dw",[m
[32m+[m[32m        "incremental",[m
[32m+[m[32m    ],[m
 )[m
 def etl_adventureworks_dw():[m
 [m
[32m+[m[32m    @task[m
[32m+[m[32m    def testar_conexoes():[m
[32m+[m[32m        """[m
[32m+[m[32m        Valida o acesso ao SQL Server de origem[m
[32m+[m[32m        e ao PostgreSQL do Data Warehouse antes[m
[32m+[m[32m        de iniciar a ETL.[m
[32m+[m[32m        """[m
[32m+[m
[32m+[m[32m        sql_server = None[m
[32m+[m[32m        postgres = None[m
[32m+[m
[32m+[m[32m        try:[m
[32m+[m[32m            sql_server = conectar_sql_server()[m
[32m+[m[32m            postgres = conectar_postgres()[m
[32m+[m
[32m+[m[32m            print([m
[32m+[m[32m                "Conexão com SQL Server validada com sucesso."[m
[32m+[m[32m            )[m
[32m+[m
[32m+[m[32m            print([m
[32m+[m[32m                "Conexão com PostgreSQL DW validada com sucesso."[m
[32m+[m[32m            )[m
[32m+[m
[32m+[m[32m            return {[m
[32m+[m[32m                "sql_server": "ok",[m
[32m+[m[32m                "postgres_dw": "ok",[m
[32m+[m[32m            }[m
[32m+[m
[32m+[m[32m        finally:[m
[32m+[m[32m            if sql_server is not None:[m
[32m+[m[32m                sql_server.close()[m
[32m+[m
[32m+[m[32m            if postgres is not None:[m
[32m+[m[32m                postgres.close()[m
[32m+[m
     @task[m
     def carregar_dim_produto():[m
         sql_server = conectar_sql_server()[m
[36m@@ -104,13 +153,25 @@[m [mdef etl_adventureworks_dw():[m
             sql_server.close()[m
             postgres.close()[m
 [m
[32m+[m[32m    inicio = testar_conexoes()[m
[32m+[m
     produto = carregar_dim_produto()[m
     territorio = carregar_dim_territorio()[m
     tempo = carregar_dim_tempo()[m
 [m
     fato = carregar_fato_venda()[m
 [m
[31m-    [produto, territorio, tempo] >> fato[m
[32m+[m[32m    inicio >> [[m
[32m+[m[32m        produto,[m
[32m+[m[32m        territorio,[m
[32m+[m[32m        tempo,[m
[32m+[m[32m    ][m
[32m+[m
[32m+[m[32m    [[m
[32m+[m[32m        produto,[m
[32m+[m[32m        territorio,[m
[32m+[m[32m        tempo,[m
[32m+[m[32m    ] >> fato[m
 [m
 [m
 etl_adventureworks_dw()[m
\ No newline at end of file[m
