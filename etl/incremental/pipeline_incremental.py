import pandas as pd

from etl.control.watermark import (
    buscar_watermark,
    atualizar_watermark
)

from etl.control.buscar_chaves_dimensoes import (
    buscar_chaves_dimensoes
)

from etl.extract.extrair_dim_produto import (
    extrair_dim_produto
)

from etl.extract.extrair_dim_territorio import (
    extrair_dim_territorio
)

from etl.extract.extrair_dim_tempo import (
    extrair_dim_tempo
)

from etl.extract.extrair_fato_venda import (
    extrair_fato_venda
)

from etl.transform.transformar_dim_produto import (
    transformar_dim_produto
)

from etl.transform.transformar_dim_territorio import (
    transformar_dim_territorio
)

from etl.transform.transformar_dim_tempo import (
    transformar_dim_tempo
)

from etl.transform.transformar_fato_venda import (
    transformar_fato_venda
)

from etl.load.carregar_dim_produto import (
    carregar_dim_produto
)

from etl.load.carregar_dim_territorio import (
    carregar_dim_territorio
)

from etl.load.carregar_dim_tempo import (
    carregar_dim_tempo
)

from etl.load.carregar_fato_venda import (
    carregar_fato_venda
)


def executar_dim_produto(
    conexao_sql_server,
    conexao_postgres
):
    """
    Executa a carga incremental de dw.dim_produto.
    """

    processo = "dim_produto"

    watermark = buscar_watermark(
        conexao_postgres,
        processo
    )

    df_extraido = extrair_dim_produto(
        conexao_sql_server,
        watermark
    )

    if df_extraido.empty:
        return {
            "processo": processo,
            "extraidos": 0,
            "processados": 0
        }

    df_transformado = transformar_dim_produto(
        df_extraido
    )

    resultado = carregar_dim_produto(
        conexao_postgres,
        df_transformado
    )

    nova_data = pd.to_datetime(
        df_extraido["ModifiedDate"],
        errors="coerce"
    ).max()

    if pd.notna(nova_data):
        atualizar_watermark(
            conexao_postgres,
            processo,
            nova_data
        )

    return {
        "processo": processo,
        "extraidos": len(df_extraido),
        "processados": resultado["processados"]
    }


def executar_dim_territorio(
    conexao_sql_server,
    conexao_postgres
):
    """
    Executa a carga incremental de dw.dim_territorio.
    """

    processo = "dim_territorio"

    watermark = buscar_watermark(
        conexao_postgres,
        processo
    )

    df_extraido = extrair_dim_territorio(
        conexao_sql_server,
        watermark
    )

    if df_extraido.empty:
        return {
            "processo": processo,
            "extraidos": 0,
            "processados": 0
        }

    df_transformado = transformar_dim_territorio(
        df_extraido
    )

    resultado = carregar_dim_territorio(
        conexao_postgres,
        df_transformado
    )

    nova_data = pd.to_datetime(
        df_extraido["ModifiedDate"],
        errors="coerce"
    ).max()

    if pd.notna(nova_data):
        atualizar_watermark(
            conexao_postgres,
            processo,
            nova_data
        )

    return {
        "processo": processo,
        "extraidos": len(df_extraido),
        "processados": resultado["processados"]
    }


def executar_dim_tempo(
    conexao_sql_server,
    conexao_postgres
):
    """
    Atualiza a dimensão tempo.

    A dimensão não utiliza watermark.
    Datas já existentes são ignoradas durante a carga.
    """

    df_extraido = extrair_dim_tempo(
        conexao_sql_server
    )

    df_transformado = transformar_dim_tempo(
        df_extraido
    )

    resultado = carregar_dim_tempo(
        conexao_postgres,
        df_transformado
    )

    return {
        "processo": "dim_tempo",
        "extraidos": len(df_extraido),
        "processados": resultado["processados"]
    }


def executar_fato_venda(
    conexao_sql_server,
    conexao_postgres
):
    """
    Executa a carga incremental de dw.fato_venda.
    """

    processo = "fato_venda"

    watermark = buscar_watermark(
        conexao_postgres,
        processo
    )

    df_extraido = extrair_fato_venda(
        conexao_sql_server,
        watermark
    )

    if df_extraido.empty:
        return {
            "processo": processo,
            "extraidos": 0,
            "processados": 0
        }

    (
        df_produto,
        df_territorio
    ) = buscar_chaves_dimensoes(
        conexao_postgres
    )

    df_transformado = transformar_fato_venda(
        df_extraido,
        df_produto,
        df_territorio
    )

    resultado = carregar_fato_venda(
        conexao_postgres,
        df_transformado
    )

    nova_data = pd.to_datetime(
        df_extraido["ModifiedDate"],
        errors="coerce"
    ).max()

    if pd.notna(nova_data):
        atualizar_watermark(
            conexao_postgres,
            processo,
            nova_data
        )

    return {
        "processo": processo,
        "extraidos": len(df_extraido),
        "processados": resultado["processados"]
    }


def executar_pipeline_incremental(
    conexao_sql_server,
    conexao_postgres
):
    """
    Executa a ETL incremental completa.

    A ordem garante que as dimensões sejam carregadas antes
    da tabela fato.
    """

    resultados = []

    resultados.append(
        executar_dim_produto(
            conexao_sql_server,
            conexao_postgres
        )
    )

    resultados.append(
        executar_dim_territorio(
            conexao_sql_server,
            conexao_postgres
        )
    )

    resultados.append(
        executar_dim_tempo(
            conexao_sql_server,
            conexao_postgres
        )
    )

    resultados.append(
        executar_fato_venda(
            conexao_sql_server,
            conexao_postgres
        )
    )

    return resultados