def buscar_watermark(conexao_postgres, processo):
    """
    Retorna a última data de execução registrada para um processo.

    Se o processo ainda não possuir watermark, retorna None.
    """

    sql = """
        SELECT ultima_execucao
        FROM controle.etl_watermark
        WHERE processo = %s
    """

    cursor = conexao_postgres.cursor()

    try:
        cursor.execute(
            sql,
            (processo,)
        )

        resultado = cursor.fetchone()

        if resultado is None:
            return None

        return resultado[0]

    finally:
        cursor.close()


def atualizar_watermark(
    conexao_postgres,
    processo,
    nova_data
):
    """
    Atualiza a data de controle de um processo ETL.
    """

    sql = """
        UPDATE controle.etl_watermark
        SET
            ultima_execucao = %s,
            atualizado_em = CURRENT_TIMESTAMP
        WHERE processo = %s
    """

    cursor = conexao_postgres.cursor()

    try:
        cursor.execute(
            sql,
            (
                nova_data,
                processo
            )
        )

        conexao_postgres.commit()

    except Exception:
        conexao_postgres.rollback()
        raise

    finally:
        cursor.close()