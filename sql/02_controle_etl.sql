-- ============================================================
-- CONTROLE DE CARGA INCREMENTAL
-- Projeto AdventureWorks Data Warehouse
-- ============================================================

CREATE SCHEMA IF NOT EXISTS controle;


CREATE TABLE IF NOT EXISTS controle.etl_watermark (
    processo VARCHAR(100) PRIMARY KEY,

    ultima_execucao TIMESTAMP NULL,

    atualizado_em TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- PROCESSOS CONTROLADOS
-- ============================================================

INSERT INTO controle.etl_watermark (
    processo,
    ultima_execucao
)
VALUES
    ('dim_produto', NULL),
    ('dim_territorio', NULL),
    ('fato_venda', NULL)

ON CONFLICT (processo)
DO NOTHING;