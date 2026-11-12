import os

import pyodbc
import psycopg2


try:
    from airflow.sdk import BaseHook
except ImportError:
    BaseHook = None


# ============================================================
# IDs das Connections cadastradas no Apache Airflow
# ============================================================

SQLSERVER_CONN_ID = "adventureworks_sqlserver"
POSTGRES_CONN_ID = "postgres_dw"


# ============================================================
# SQL SERVER
# ============================================================

def conectar_sql_server():
    """
    Cria conexão com o SQL Server que contém o AdventureWorks.

    Prioridade:
    1. Airflow Connection 'adventureworks_sqlserver'
    2. Variáveis de ambiente como fallback

    O fallback permite que a ETL continue podendo ser executada
    manualmente fora do contexto do Apache Airflow.
    """

    # --------------------------------------------------------
    # Tenta utilizar a Connection cadastrada no Airflow
    # --------------------------------------------------------

    if BaseHook is not None:
        try:
            conexao_airflow = BaseHook.get_connection(
                SQLSERVER_CONN_ID
            )

            extras = conexao_airflow.extra_dejson

            driver = extras.get(
                "driver",
                "ODBC Driver 18 for SQL Server"
            )

            encrypt = extras.get(
                "Encrypt",
                "no"
            )

            trust_certificate = extras.get(
                "TrustServerCertificate",
                "yes"
            )

            application_intent = extras.get(
                "ApplicationIntent",
                "ReadOnly"
            )

            string_conexao = (
                f"DRIVER={{{driver}}};"
                f"SERVER={conexao_airflow.host},"
                f"{conexao_airflow.port or 1433};"
                f"DATABASE={conexao_airflow.schema};"
                f"UID={conexao_airflow.login};"
                f"PWD={conexao_airflow.password};"
                f"Encrypt={encrypt};"
                f"TrustServerCertificate={trust_certificate};"
                f"ApplicationIntent={application_intent};"
            )

            print(
                "Conexão SQL Server obtida pelo Airflow: "
                f"{SQLSERVER_CONN_ID}"
            )

            return pyodbc.connect(
                string_conexao
            )

        except Exception as erro:
            print(
                "Não foi possível utilizar a Airflow Connection "
                f"'{SQLSERVER_CONN_ID}'. "
                "Tentando variáveis de ambiente."
            )

            print(
                f"Detalhe: {type(erro).__name__}"
            )

    # --------------------------------------------------------
    # Fallback pelas variáveis de ambiente
    # --------------------------------------------------------

    driver = os.getenv(
        "SQLSERVER_DRIVER",
        "ODBC Driver 18 for SQL Server"
    )

    host = os.getenv(
        "SQLSERVER_HOST",
        "host.docker.internal"
    )

    port = os.getenv(
        "SQLSERVER_PORT",
        "1433"
    )

    database = os.getenv(
        "SQLSERVER_DATABASE",
        "AdventureWorks2016"
    )

    usuario = os.getenv(
        "SQLSERVER_USER"
    )

    senha = os.getenv(
        "SQLSERVER_PASSWORD"
    )

    if not usuario or not senha:
        raise RuntimeError(
            "Não foi possível obter as credenciais do SQL Server "
            "pelo Airflow nem pelas variáveis de ambiente."
        )

    string_conexao = (
        f"DRIVER={{{driver}}};"
        f"SERVER={host},{port};"
        f"DATABASE={database};"
        f"UID={usuario};"
        f"PWD={senha};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
        "ApplicationIntent=ReadOnly;"
    )

    print(
        "Conexão SQL Server obtida pelas variáveis "
        "de ambiente."
    )

    return pyodbc.connect(
        string_conexao
    )


# ============================================================
# POSTGRESQL DATA WAREHOUSE
# ============================================================

def conectar_postgres():
    """
    Cria conexão com o PostgreSQL que armazena o Data Warehouse.

    Prioridade:
    1. Airflow Connection 'postgres_dw'
    2. Variáveis de ambiente como fallback

    O fallback permite que a ETL continue podendo ser executada
    manualmente fora do contexto do Apache Airflow.
    """

    # --------------------------------------------------------
    # Tenta utilizar a Connection cadastrada no Airflow
    # --------------------------------------------------------

    if BaseHook is not None:
        try:
            conexao_airflow = BaseHook.get_connection(
                POSTGRES_CONN_ID
            )

            print(
                "Conexão PostgreSQL obtida pelo Airflow: "
                f"{POSTGRES_CONN_ID}"
            )

            return psycopg2.connect(
                host=conexao_airflow.host,
                port=conexao_airflow.port or 5432,
                database=conexao_airflow.schema,
                user=conexao_airflow.login,
                password=conexao_airflow.password
            )

        except Exception as erro:
            print(
                "Não foi possível utilizar a Airflow Connection "
                f"'{POSTGRES_CONN_ID}'. "
                "Tentando variáveis de ambiente."
            )

            print(
                f"Detalhe: {type(erro).__name__}"
            )

    # --------------------------------------------------------
    # Fallback pelas variáveis de ambiente
    # --------------------------------------------------------

    host = os.getenv(
        "DW_POSTGRES_HOST",
        "postgres-dw"
    )

    port = os.getenv(
        "DW_POSTGRES_PORT",
        "5432"
    )

    database = os.getenv(
        "DW_POSTGRES_DB",
        "adventureworks_dw"
    )

    usuario = os.getenv(
        "DW_POSTGRES_USER"
    )

    senha = os.getenv(
        "DW_POSTGRES_PASSWORD"
    )

    if not usuario or not senha:
        raise RuntimeError(
            "Não foi possível obter as credenciais do PostgreSQL "
            "pelo Airflow nem pelas variáveis de ambiente."
        )

    print(
        "Conexão PostgreSQL obtida pelas variáveis "
        "de ambiente."
    )

    return psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=usuario,
        password=senha
    )