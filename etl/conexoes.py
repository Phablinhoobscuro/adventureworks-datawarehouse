import os

import pyodbc
import psycopg2


def conectar_sql_server():
    """
    Cria conexão com o SQL Server que contém o AdventureWorks.

    As configurações são obtidas por variáveis de ambiente.
    """

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
            "SQLSERVER_USER e SQLSERVER_PASSWORD "
            "não foram configurados."
        )

    string_conexao = (
        f"DRIVER={{{driver}}};"
        f"SERVER={host},{port};"
        f"DATABASE={database};"
        f"UID={usuario};"
        f"PWD={senha};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(
        string_conexao
    )


def conectar_postgres():
    """
    Cria conexão com o PostgreSQL que armazenará o Data Warehouse.

    As configurações são obtidas por variáveis de ambiente.
    """

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
            "DW_POSTGRES_USER e DW_POSTGRES_PASSWORD "
            "não foram configurados."
        )

    return psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=usuario,
        password=senha
    )