# Revisão do Material Disponibilizado pelo Professor

## 1. Objetivo

Este documento registra a revisão técnica do material disponibilizado pelo professor no diretório:

```text
unisales.etl.20262-main/aula.etl.2
```

O objetivo da revisão foi validar se a base fornecida é executável, identificar quais componentes podem ser reutilizados diretamente no projeto individual, quais precisam de adaptação e quais devem permanecer apenas como referência didática.

---

## 2. Validação prática da base fornecida

A base foi executada inicialmente sem alterações estruturais, com o objetivo de verificar se o ambiente fornecido pelo professor funcionava corretamente antes de qualquer adaptação.

Foram realizadas as seguintes etapas:

1. criação das pastas `logs`, `plugins`, `config` e `data`;
2. criação do arquivo `.env` a partir de `.env.example`;
3. geração das chaves de segurança utilizadas pelo Airflow;
4. validação do `docker-compose.yml`;
5. execução do `airflow-init`;
6. inicialização dos serviços com Docker Compose;
7. acesso à interface web do Apache Airflow;
8. autenticação com o usuário administrador;
9. execução manual de uma DAG de exemplo;
10. validação da persistência de dados em volume local.

O ambiente foi inicializado com sucesso e os principais serviços ficaram disponíveis:

```text
postgres
airflow-apiserver
airflow-scheduler
airflow-triggerer
airflow-dag-processor
```

O serviço `airflow-init` foi executado corretamente e encerrado com código 0 após inicializar o ambiente e criar o usuário administrador.

---

## 3. Resultado da execução da DAG de exemplo

A DAG utilizada para validação foi:

```text
etl_exemplo_persistencia_local
```

As tasks executadas foram:

```text
extrair
transformar
transformar2
persistir
```

Todas as tasks terminaram com status de sucesso.

Fluxo validado:

```text
extrair
   |
   +------------+
   |            |
   v            v
transformar  transformar2
   |
   v
persistir
```

Também foi criado corretamente o arquivo:

```text
data/resultado_etl.json
```

A execução comprovou que a base fornecida pelo professor suporta:

- criação e carregamento de DAGs;
- execução de tasks Python;
- definição de dependências;
- execução manual de pipelines;
- persistência de arquivos em volume Docker;
- uso da interface web do Apache Airflow.

---

## 4. Classificação dos componentes

Os componentes foram classificados em três grupos:

- reutilizar;
- adaptar;
- manter apenas como referência.

---

## 5. Componentes reutilizáveis diretamente

### Apache Airflow 3.3.1

O ambiente utiliza Apache Airflow 3.3.1 e foi executado com sucesso.

Decisão:

```text
REUTILIZAR
```

Será utilizado como ferramenta de orquestração da ETL do projeto AdventureWorks.

---

### PostgreSQL 16

O ambiente utiliza PostgreSQL 16 como banco de metadados do Airflow.

Decisão:

```text
REUTILIZAR
```

Esse banco permanecerá responsável pelos metadados internos do Apache Airflow.

O Data Warehouse AdventureWorks deverá utilizar um PostgreSQL separado.

---

### LocalExecutor

O ambiente está configurado com:

```text
LocalExecutor
```

Decisão:

```text
REUTILIZAR
```

O executor é suficiente para o ambiente acadêmico e execução local do projeto.

---

### Estrutura Docker

O ambiente Docker fornecido foi validado com sucesso.

Decisão:

```text
REUTILIZAR COMO BASE
```

A arquitetura geral será mantida e complementada.

---

## 6. Componentes que serão adaptados

### docker-compose.yml

O arquivo atual cria a infraestrutura necessária ao Apache Airflow, incluindo:

- PostgreSQL;
- Airflow API Server;
- Scheduler;
- Triggerer;
- DAG Processor;
- inicialização do ambiente.

Decisão:

```text
ADAPTAR
```

O arquivo será utilizado como base e deverá receber um novo serviço PostgreSQL dedicado ao Data Warehouse.

Arquitetura esperada:

```text
Docker
│
├── PostgreSQL Airflow
│   └── banco airflow
│
├── PostgreSQL Data Warehouse
│   └── adventureworks_dw
│
└── Apache Airflow
    ├── API Server
    ├── Scheduler
    ├── DAG Processor
    └── Triggerer
```

---

### .env.example

O arquivo contém configurações do ambiente e dependências adicionais do Airflow.

Decisão:

```text
ADAPTAR
```

Será utilizado como referência para o projeto atual, com inclusão de variáveis relacionadas ao PostgreSQL do Data Warehouse e às conexões necessárias.

Credenciais reais continuarão armazenadas apenas no arquivo `.env`, que não será versionado.

---

### Padrão @dag e @task

As DAGs fornecidas demonstram a utilização de:

```python
@dag
@task
```

Decisão:

```text
ADAPTAR AO ADVENTUREWORKS
```

Esse padrão será utilizado na construção das DAGs do projeto individual.

Exemplo conceitual esperado:

```text
extrair_adventureworks
        ↓
transformar_vendas
        ↓
carregar_dimensoes
        ↓
carregar_fato
        ↓
atualizar_controle_incremental
```

---

### SQLExecuteQueryOperator

O material utiliza o operador:

```text
SQLExecuteQueryOperator
```

Decisão:

```text
ADAPTAR
```

Esse padrão poderá ser utilizado para executar scripts SQL do projeto, incluindo o modelo físico do Data Warehouse e outras tarefas SQL.

---

## 7. Componentes utilizados somente como referência

### etl_exemplo.py

A DAG foi executada com sucesso e demonstrou:

- uso de `@dag`;
- uso de `@task`;
- dependências entre tasks;
- passagem de dados entre tarefas;
- persistência local.

Decisão:

```text
REFERÊNCIA
```

O arquivo não será copiado diretamente para o projeto AdventureWorks, mas servirá como modelo de implementação.

---

### etl_build_schema_dw.py

O arquivo demonstra o uso de:

```text
SQLExecuteQueryOperator
```

para criação de estruturas SQL.

Decisão:

```text
REFERÊNCIA / ADAPTAÇÃO CONCEITUAL
```

A lógica poderá ser adaptada para executar scripts do Data Warehouse AdventureWorks.

---

### etl_build_schema_stg.py

O arquivo demonstra a criação de uma camada de staging.

Decisão:

```text
REFERÊNCIA
```

O projeto individual não possui obrigação explícita de implementar staging nesse formato. A necessidade será avaliada durante a adaptação da ETL existente.

---

### extract_blockbuster.py

O arquivo trabalha com dados do domínio Blockbuster e possui lógica específica do exemplo da disciplina.

Decisão:

```text
REFERÊNCIA
```

Não será reutilizado diretamente no AdventureWorks.

---

### dags/sql/

Os scripts SQL existentes nesse diretório estão relacionados ao domínio utilizado nos exemplos do professor.

Decisão:

```text
NÃO COPIAR
```

Os scripts SQL oficiais do projeto individual já estão consolidados na pasta:

```text
sql/
```

do repositório AdventureWorks.

---

## 8. Dependências do ambiente

O arquivo `.env.example` do professor inclui dependências adicionais como:

```text
apache-airflow-providers-postgres
apache-airflow-providers-http
requests
pandas
```

Essas dependências serão mantidas quando aplicáveis.

Como a origem do projeto AdventureWorks será Microsoft SQL Server, será necessário posteriormente adicionar o suporte correspondente à comunicação entre Airflow e SQL Server.

A dependência exata será definida somente após a revisão da ETL Python existente.

---

## 9. Resultado da revisão

A classificação final do material é:

```text
REUTILIZAR
├── Apache Airflow 3.3.1
├── PostgreSQL 16 para metadados
├── LocalExecutor
└── estrutura Docker

ADAPTAR
├── docker-compose.yml
├── .env.example
├── padrão @dag/@task
└── padrão SQLExecuteQueryOperator

SOMENTE REFERÊNCIA
├── etl_exemplo.py
├── etl_build_schema_dw.py
├── etl_build_schema_stg.py
├── extract_blockbuster.py
└── scripts SQL do domínio de exemplo
```

---

## 10. Conclusão

O material disponibilizado pelo professor foi validado tecnicamente e executado com sucesso sem necessidade de alterações estruturais iniciais.

A base é adequada para servir como infraestrutura do projeto individual e reduz significativamente o trabalho de configuração do Apache Airflow.

A estratégia adotada será:

```text
Infraestrutura do professor
        +
ETL existente do AdventureWorks
        ↓
Adaptação e integração
        ↓
Pipeline incremental orquestrada
        ↓
Testes + KPIs + documentação + artigo
```

A próxima atividade da Fase 2 será revisar e consolidar a ETL Python do projeto anterior AdventureWorks antes de integrar os dois conjuntos de materiais.
