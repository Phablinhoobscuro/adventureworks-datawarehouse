# Consolidação dos Scripts SQL Reutilizados

## 1. Objetivo

Este documento registra a análise e consolidação dos scripts SQL provenientes do projeto anterior AdventureWorks.

A finalidade foi identificar quais arquivos permanecem válidos para o projeto individual, adaptar os scripts à versão oficial do modelo multidimensional e eliminar versões antigas ou redundantes.

---

## 2. Scripts analisados

| Arquivo original | Decisão |
|---|---|
| `01_modelo_fisico_dw_postgresql.sql` | Reutilizado e revisado |
| `Top10KPIs.sql` | Reutilizado e consolidado como `04_kpis.sql` |
| `New_modelo_fisico_dw.sql` | Não reutilizado |
| `AdventureWorks2016.bak` | Não versionado |

---

## 3. Modelo físico oficial

O arquivo oficial do modelo físico é:

```text
sql/01_modelo_fisico_dw_postgresql.sql
```

O modelo utiliza o schema `dw` e contém:

- `dw.dim_tempo`;
- `dw.dim_produto`;
- `dw.dim_territorio`;
- `dw.fato_venda`.

A granularidade da tabela fato é:

> Uma linha representa um item de pedido de venda.

O modelo utiliza:

- chaves substitutas nas dimensões Produto e Território;
- chave temporal controlada pela ETL;
- chaves estrangeiras;
- restrições `UNIQUE`;
- restrições `CHECK`;
- membros técnicos `-1`;
- índices nas chaves estrangeiras da tabela fato;
- dimensão degenerada para `sales_order_id`;
- estratégia Slowly Changing Dimension Tipo 1.

### Ajustes realizados no modelo físico

Durante a revisão foram realizados os seguintes ajustes:

1. inclusão de documentação explícita da estratégia **SCD Tipo 1**;
2. manutenção do grão de um item por pedido;
3. manutenção dos membros técnicos `-1`;
4. manutenção das regras de qualidade e integridade;
5. remoção do índice isolado de `sales_order_id`, considerado redundante porque a constraint:

```text
UNIQUE (sales_order_id, sales_order_detail_id)
```

já cria um índice B-tree cujo primeiro campo é `sales_order_id`.

O controle operacional da ETL incremental não foi incluído dentro do schema `dw`. Esse controle será tratado separadamente na etapa de adaptação da ETL.

---

## 4. Indicadores

O arquivo original `Top10KPIs.sql` foi consolidado como:

```text
sql/04_kpis.sql
```

Ele contém os dez indicadores definidos para o projeto:

1. Receita de vendas;
2. Quantidade total de itens vendidos;
3. Quantidade de pedidos;
4. Ticket médio;
5. Desconto total concedido;
6. Percentual de desconto sobre o valor bruto;
7. Margem bruta;
8. Margem bruta percentual;
9. Receita por produto;
10. Receita por território.

### Ajustes realizados nas consultas

As consultas do projeto anterior utilizavam nomes pertencentes a uma versão antiga do modelo, como:

```text
dw.fato_vendas
receita
valor_bruto
produto_key
territorio_key
product_id
territory_id
pais
grupo
```

Esses nomes foram substituídos pelos atributos oficiais do modelo consolidado:

```text
dw.fato_venda
valor_receita
valor_bruto_item
sk_produto
sk_territorio
product_id_oltp
territory_id_oltp
codigo_pais
grupo_territorial
```

O KPI 6 também teve sua nomenclatura ajustada de "percentual médio de desconto" para:

> **Percentual de desconto sobre o valor bruto**

Isso representa com maior precisão a fórmula utilizada:

```text
SUM(valor_desconto)
------------------------- x 100
SUM(valor_bruto_item)
```

O indicador mede o impacto financeiro global dos descontos sobre o valor bruto vendido.

---

## 5. Compatibilidade entre o modelo e os KPIs

Após a revisão, os dez indicadores possuem suporte direto no modelo físico.

| KPI | Principais campos utilizados |
|---|---|
| Receita de vendas | `valor_receita` |
| Itens vendidos | `quantidade` |
| Quantidade de pedidos | `sales_order_id` |
| Ticket médio | `valor_receita`, `sales_order_id` |
| Desconto total | `valor_desconto` |
| Percentual de desconto | `valor_desconto`, `valor_bruto_item` |
| Margem bruta | `margem_bruta` |
| Margem bruta percentual | `margem_bruta`, `valor_receita` |
| Receita por produto | `sk_produto`, `valor_receita` |
| Receita por território | `sk_territorio`, `valor_receita` |

---

## 6. Script não reutilizado

O arquivo `New_modelo_fisico_dw.sql` não foi incorporado ao projeto individual.

Ele representa uma versão alternativa da modelagem e contém diferenças em relação ao Star Schema adotado, incluindo:

- `dim_data` no lugar de `dim_tempo`;
- inclusão de `dim_cliente`;
- `fato_vendas` no lugar de `fato_venda`;
- nomes de chaves diferentes;
- atributos diferentes;
- tabela de controle ETL dentro do schema `dw`.

Manter duas versões concorrentes do modelo físico poderia gerar inconsistências entre o Data Warehouse, a ETL e os KPIs.

---

## 7. Backup AdventureWorks

O arquivo `AdventureWorks2016.bak` não será versionado no repositório individual.

O backup é utilizado apenas para restauração do banco OLTP de origem e está coberto pelo `.gitignore` por meio da regra:

```text
*.bak
```

---

## 8. Resultado da consolidação

Ao final da tarefa, a pasta SQL oficial do projeto contém:

```text
sql/
├── 01_modelo_fisico_dw_postgresql.sql
└── 04_kpis.sql
```

Esses arquivos passam a representar a versão oficial do modelo multidimensional e das consultas analíticas do projeto individual.

### Status

```text
01_modelo_fisico_dw_postgresql.sql  -> APROVADO
04_kpis.sql                         -> APROVADO
```

A próxima etapa da Fase 2 será a consolidação da ETL Python reutilizável.
