## 🧭 Visão Geral

O projeto implementa um pipeline de dados dividido em três camadas clássicas:

- **RAW** → Ingestão dos dados brutos  
- **STAGE** → Limpeza, padronização e pré-processamento  
- **ANALYTICS** → Modelagem final e preparação para consumo analítico

## 📂 Estrutura do Projeto

```
.
├── data_pipeline/
│   ├── scripts/        # Scripts dos pipelines RAW, Stage e Analytics
│   ├── tools/          # Funções auxiliares e validadores
│   ├── tests/          # Testes automatizados (pytest)
│   ├── configs/        # Configurações e variáveis
│   └── __init__.py
├── data_base/          # Dados de entrada do desafio
├── docker-compose.yml  # Orquestração da aplicação + LocalStack
├── Dockerfile          # Ambiente com Spark + Python
└── README.md           # Este arquivo
```

## 🐳 Execução Local (Docker + LocalStack)

### 1. Construir a imagem

```bash
docker compose build
```

### 2. Subir os serviços

```bash
docker compose up -d
```

### 3. Entrar no container da aplicação

```bash
docker exec -it spark-pipeline bash
```

### 4. Executar os testes

```bash
pytest -q data_pipeline/tests
```

### 5. Executar o Pipeline RAW

```bash
python -m data_pipeline.scripts.pipeline_raw --env local --output-dir ./local_output
```

Os arquivos gerados aparecerão em:

```
./local_output/
```

## ⭐ Observações Importantes

- O projeto usa LocalStack para simular AWS S3/Glue localmente.
- O uso de Parquet nas camadas STAGE/ANALYTICS foi adotado para manter simplicidade.
- O arquivo de entrada `data_base/dados_entrada.xlsx` já está incluído.

## Logs dos testes

<img width="1291" height="459" alt="Captura de tela 2025-11-23 174951" src="https://github.com/user-attachments/assets/f39262ce-6126-4fc4-b7b1-c1b5fe551852" />


## Objetivo

Este projeto implementa um pipeline ETL moderno utilizando Python, Pandas, PySpark e arquitetura Data Lake em três camadas:

* RAW → Ingestão e validação
* STAGE → Tratamento e deduplicação
* ANALYTICS → Modelagem para consumo analítico

O objetivo é transformar dados brutos de clientes e endereços em uma camada pronta para análises e dashboards.

---

# Arquitetura

```text
Excel (GitHub)
      │
      ▼
    RAW
(Extração + Validação)
      │
      ▼
   STAGE
(Deduplicação)
      │
      ▼
 ANALYTICS
(Join + Regras de Negócio)
      │
      ▼
 Consumo Analítico
```

---

# Estrutura do Projeto

```text
etl/
│
├── data_base/
│   └── dados_entrada.xlsx
│
├── data_pipeline/
│   ├── configs/
│   ├── scripts/
│   ├── tools/
│   └── tests/
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Componentes Principais

## extract.py

Responsável por:

* Baixar o Excel do GitHub
* Ler as planilhas
* Converter para DataFrames Pandas

Planilhas processadas:

```text
clientes
enderecos
```

Fluxo:

```text
Excel → DataFrames
```

---

## pipeline_raw.py

Responsável por:

* Executar a ingestão
* Aplicar validações
* Separar registros válidos e inválidos
* Salvar dados na camada RAW

Fluxo:

```text
Excel
 │
 ▼
Validação
 │
 ├── Válidos
 │
 └── Inválidos
      │
      ▼
RAW
```

Principais etapas:

1. Extração dos dados
2. Validação de clientes
3. Validação de endereços
4. Separação de erros
5. Persistência dos dados

---

## pipeline_stage.py

Responsável por:

* Ler os dados da camada RAW
* Remover duplicidades
* Preparar dados para modelagem

Fluxo:

```text
RAW
 │
 ▼
Deduplicação
 │
 ▼
STAGE
```

Regras aplicadas:

### Clientes

```text
Mantém apenas o registro mais recente
por id_cliente
```

### Endereços

```text
Mantém apenas o registro mais recente
por id_endereco
```

---

## pipeline_analytics.py

Responsável por:

* Aplicar regras de negócio
* Criar dataset analítico final

Fluxo:

```text
STAGE
 │
 ▼
Join
 │
 ▼
Transformações
 │
 ▼
ANALYTICS
```

Transformações executadas:

### Filtragem

Mantém apenas:

```text
status = ativo
```

### Enriquecimento

Calcula:

```text
idade
```

a partir de:

```text
data_nascimento
```

### Integração

Executa:

```text
LEFT JOIN
```

entre:

```text
clientes
+
enderecos
```

---

# Pipeline RAW

## Entrada

```text
dados_entrada.xlsx
```

## Processamento

```text
Extração
      │
      ▼
Validação
      │
      ▼
Separação
      │
      ▼
Persistência
```

## Saída

```text
raw/
├── clientes/
├── clientes_invalidos/
├── enderecos/
└── enderecos_invalidos/
```

---

# Pipeline STAGE

## Entrada

```text
raw/clientes
raw/enderecos
```

## Processamento

```text
Deduplicação
```

## Saída

```text
stage/
├── clientes/
└── enderecos/
```

---

# Pipeline ANALYTICS

## Entrada

```text
stage/clientes
stage/enderecos
```

## Processamento

```text
Filtro de ativos
        │
        ▼
LEFT JOIN
        │
        ▼
Cálculo da idade
        │
        ▼
Otimização
```

## Saída

```text
analytics/
└── clientes/
```

---

# Fluxo Completo

```text
Excel
 │
 ▼
Extract
 │
 ▼
Pipeline RAW
 │
 ▼
RAW
 │
 ▼
Pipeline STAGE
 │
 ▼
STAGE
 │
 ▼
Pipeline ANALYTICS
 │
 ▼
Analytics
 │
 ▼
Dashboard / BI / Data Science
```

---

# Tecnologias Utilizadas

### Processamento

* Python
* Pandas
* PySpark

### Armazenamento

* Parquet

### Infraestrutura

* Docker
* Docker Compose
* LocalStack (AWS local)

### Testes

* Pytest

---

# Resumo Executivo

O projeto segue uma arquitetura Data Lake em três camadas:

### RAW

Captura e valida os dados de origem.

### STAGE

Remove duplicidades e padroniza os dados.

### ANALYTICS

Aplica regras de negócio, realiza integrações e gera datasets prontos para análise.

O resultado final é uma tabela analítica consolidada contendo clientes ativos, seus endereços e atributos derivados (como idade), pronta para consumo por ferramentas de BI, Data Science ou Machine Learning.
