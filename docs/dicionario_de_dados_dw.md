# Dicionário de Dados — Data Warehouse AdventureWorks

## 1. Escopo

Este documento descreve o modelo dimensional implementado no schema `dw` do banco PostgreSQL `adventureworks_dw`.

O modelo é composto por três dimensões e uma tabela fato:

- `dw.dim_produto`
- `dw.dim_tempo`
- `dw.dim_territorio`
- `dw.fato_venda`

A granularidade da tabela fato é:

> **1 linha em `dw.fato_venda` = 1 item de pedido de venda.**

O grão é protegido pela restrição `UNIQUE (sales_order_id, sales_order_detail_id)`.

As dimensões `dim_produto` e `dim_territorio` possuem membro técnico `-1`, utilizado para representar registros desconhecidos ou não encontrados durante a carga.

---

## 2. dw.dim_produto

**Finalidade:** armazenar atributos descritivos de produtos utilizados nas análises de vendas.

**Estratégia dimensional:** SCD Tipo 1.

| Coluna | Tipo | Nulo? | Chave/Restrição | Origem/Derivação | Descrição |
|---|---|---:|---|---|---|
| `sk_produto` | `integer` | Não | PK | Gerada no DW | Chave substituta da dimensão produto. |
| `product_id_oltp` | `integer` | Não | UNIQUE | `Production.Product.ProductID` | Identificador do produto no AdventureWorks. |
| `nome_produto` | `varchar(100)` | Não | — | `Production.Product.Name` | Nome descritivo do produto. |
| `numero_produto` | `varchar(25)` | Não | — | `Production.Product.ProductNumber` | Código/número comercial do produto. |
| `cor` | `varchar(15)` | Sim | — | `Production.Product.Color` | Cor do produto. Quando ausente, a ETL pode padronizar o valor. |
| `tamanho` | `varchar(10)` | Sim | — | `Production.Product.Size` | Tamanho do produto. Quando ausente, a ETL utiliza valor padronizado. |
| `nome_subcategoria` | `varchar(50)` | Não | — | `Production.ProductSubcategory.Name` | Nome da subcategoria do produto; quando não classificado, recebe valor padrão. |
| `nome_categoria` | `varchar(50)` | Não | — | `Production.ProductCategory.Name` | Nome da categoria do produto; quando não classificado, recebe valor padrão. |
| `preco_lista` | `numeric(19,4)` | Não | CHECK `>= 0` | `Production.Product.ListPrice` | Preço de lista do produto. |

### Membro técnico

A dimensão contém o membro técnico:

- `sk_produto = -1`
- `product_id_oltp = -1`
- descrição: `Não informado`

Esse membro permite manter a integridade referencial caso uma venda não encontre correspondência válida na dimensão.

---

## 3. dw.dim_tempo

**Finalidade:** representar datas e atributos calendários utilizados nas análises temporais.

**Geração:** dimensão determinística criada a partir do período existente nas vendas do AdventureWorks.

| Coluna | Tipo | Nulo? | Chave/Restrição | Origem/Derivação | Descrição |
|---|---|---:|---|---|---|
| `sk_tempo` | `integer` | Não | PK | Data no formato `YYYYMMDD` | Chave da dimensão tempo. |
| `data_completa` | `date` | Não | UNIQUE | Data do calendário | Data completa correspondente ao registro. |
| `dia` | `smallint` | Não | CHECK `1..31` | Derivado da data | Dia do mês. |
| `mes` | `smallint` | Não | CHECK `1..12` | Derivado da data | Número do mês. |
| `nome_mes` | `varchar(20)` | Não | — | Derivado da data | Nome do mês em português. |
| `trimestre` | `smallint` | Não | CHECK `1..4` | Derivado da data | Trimestre do ano. |
| `ano` | `smallint` | Não | CHECK `> 0` | Derivado da data | Ano calendário. |
| `dia_semana` | `smallint` | Não | CHECK `1..7` | Derivado da data | Número do dia da semana, com segunda-feira como 1. |
| `nome_dia_semana` | `varchar(20)` | Não | — | Derivado da data | Nome do dia da semana em português. |
| `semana_ano` | `smallint` | Não | CHECK `1..53` | Semana ISO | Número da semana no ano. |
| `fim_de_semana` | `boolean` | Não | — | Derivado da data | Indica se a data corresponde a sábado ou domingo. |

---

## 4. dw.dim_territorio

**Finalidade:** armazenar os territórios comerciais associados às vendas.

**Estratégia dimensional:** SCD Tipo 1.

| Coluna | Tipo | Nulo? | Chave/Restrição | Origem/Derivação | Descrição |
|---|---|---:|---|---|---|
| `sk_territorio` | `integer` | Não | PK | Gerada no DW | Chave substituta da dimensão território. |
| `territory_id_oltp` | `integer` | Não | UNIQUE | `Sales.SalesTerritory.TerritoryID` | Identificador do território no AdventureWorks. |
| `nome_territorio` | `varchar(50)` | Não | — | `Sales.SalesTerritory.Name` | Nome do território comercial. |
| `codigo_pais` | `varchar(3)` | Não | — | `Sales.SalesTerritory.CountryRegionCode` | Código do país/região. |
| `grupo_territorial` | `varchar(50)` | Não | — | `Sales.SalesTerritory.Group` | Grupo geográfico ao qual o território pertence. |

### Membro técnico

A dimensão contém o membro técnico:

- `sk_territorio = -1`
- `territory_id_oltp = -1`
- descrição: `Não informado`

Esse membro é utilizado quando a chave territorial de origem não pode ser resolvida.

---

## 5. dw.fato_venda

**Finalidade:** armazenar as medidas quantitativas e financeiras de cada item de pedido de venda.

**Granularidade:** uma linha por item de pedido de venda.

| Coluna | Tipo | Nulo? | Chave/Restrição | Origem/Derivação | Descrição |
|---|---|---:|---|---|---|
| `sk_venda` | `bigint` | Não | PK | Gerada no DW | Chave substituta da linha da fato. |
| `sales_order_id` | `integer` | Não | CHECK `> 0` | `Sales.SalesOrderHeader.SalesOrderID` | Identificador do pedido de venda. |
| `sales_order_detail_id` | `integer` | Não | CHECK `> 0` | `Sales.SalesOrderDetail.SalesOrderDetailID` | Identificador do item do pedido. |
| `sk_tempo` | `integer` | Não | FK → `dim_tempo.sk_tempo` | Derivada de `OrderDate` | Chave da dimensão tempo. |
| `sk_produto` | `integer` | Não | FK → `dim_produto.sk_produto` | Lookup por `ProductID` | Chave da dimensão produto; pode usar `-1` quando não encontrada. |
| `sk_territorio` | `integer` | Não | FK → `dim_territorio.sk_territorio` | Lookup por `TerritoryID` | Chave da dimensão território; pode usar `-1` quando não encontrada. |
| `quantidade` | `integer` | Não | CHECK `> 0` | `Sales.SalesOrderDetail.OrderQty` | Quantidade vendida no item. |
| `preco_unitario` | `numeric(19,4)` | Não | CHECK `>= 0` | `Sales.SalesOrderDetail.UnitPrice` | Preço unitário praticado no item. |
| `percentual_desconto_item` | `numeric(9,6)` | Não | CHECK `0..1` | `Sales.SalesOrderDetail.UnitPriceDiscount` | Percentual de desconto aplicado ao item. |
| `valor_receita` | `numeric(20,6)` | Não | CHECK `>= 0` | `Sales.SalesOrderDetail.LineTotal` | Receita líquida do item após desconto. |
| `valor_bruto_item` | `numeric(20,6)` | Não | CHECK `>= 0` | `quantidade × preco_unitario` | Valor bruto do item antes do desconto. |
| `valor_desconto` | `numeric(20,6)` | Não | CHECK `>= 0` e `<= valor_bruto_item` | `quantidade × preco_unitario × desconto` | Valor financeiro concedido como desconto. |
| `custo_unitario_aplicado` | `numeric(19,4)` | Não | CHECK `>= 0` | Histórico de custo / custo atual | Custo unitário utilizado para o cálculo de margem. |
| `origem_custo` | `varchar(20)` | Não | CHECK em `HISTORICO`, `FALLBACK_ATUAL` | Derivado na ETL | Indica se o custo veio do histórico válido ou do custo atual de fallback. |
| `custo_total` | `numeric(20,6)` | Não | CHECK `>= 0` | `quantidade × custo_unitario_aplicado` | Custo total do item vendido. |
| `margem_bruta` | `numeric(20,6)` | Não | — | `valor_receita - custo_total` | Margem bruta financeira do item. |

### Restrição de granularidade

A tabela possui:

```sql
UNIQUE (sales_order_id, sales_order_detail_id)
```

Essa restrição impede que o mesmo item de pedido seja gravado mais de uma vez.

---

## 6. Relacionamentos do Star Schema

| Tabela fato | Dimensão | Relacionamento |
|---|---|---|
| `fato_venda.sk_tempo` | `dim_tempo.sk_tempo` | Muitos para um |
| `fato_venda.sk_produto` | `dim_produto.sk_produto` | Muitos para um |
| `fato_venda.sk_territorio` | `dim_territorio.sk_territorio` | Muitos para um |

---

## 7. Índices relevantes

Além dos índices criados automaticamente pelas PKs e restrições UNIQUE, a tabela `fato_venda` possui índices explícitos para as chaves estrangeiras:

- `idx_fato_venda_sk_produto`
- `idx_fato_venda_sk_tempo`
- `idx_fato_venda_sk_territorio`

Esses índices favorecem os joins entre a tabela fato e as dimensões em consultas analíticas.

---

## 8. Resumo de validação

- 4 tabelas no schema `dw`;
- 41 colunas validadas;
- 29 constraints identificadas;
- 11 índices identificados;
- 3 chaves estrangeiras na tabela fato;
- membros técnicos `-1` validados em produto e território;
- 121.317 linhas na `fato_venda`;
- 121.317 grãos distintos;
- 0 duplicidades no grão;
- 0 valores nulos nas chaves e medidas essenciais avaliadas.

**Status do dicionário:** atualizado e compatível com o modelo físico efetivamente implementado no PostgreSQL.
