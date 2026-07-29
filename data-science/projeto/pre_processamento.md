# Pré-processamento de Dados

## Visão Geral
Esta etapa realiza a extração, transformação e carga (ETL) dos dados brutos, preparando-os para análise e modelagem de machine learning.

## Ferramentas Selecionadas

### Python 3.x
Linguagem principal do projeto, escolhida por seu vasto ecossistema em ciência de dados e machine learning.

### Bibliotecas
- **PySpark**: Processamento distribuído de grandes volumes de dados
- **Boto3**: SDK da AWS para integração com S3
- **Requests**: Cliente HTTP para download de arquivos

### Infraestrutura
- **Amazon S3**: Armazenamento em camadas (raw, staging, processed)

## Pipeline de Processamento

### 1. Extração (extracao.py)
- Download do arquivo ZIP do GitHub
- Upload para S3 na camada `raw/`

### 2. Transformação e Carga (transformacao_carga.py)
- Limpeza da pasta `staging_raw/`
- Descompactação do ZIP diretamente no S3
- Leitura dos CSVs com Spark
- Inferência automática de schema
- Conversão para formato Parquet
- Salvamento na camada `processed/`

## Ações de Limpeza e Padronização

- **Consolidação**: Unificação de múltiplos CSVs em dataset único
- **Conversão para Parquet**: Formato colunar otimizado, redução de tamanho e melhor performance
- **Inferência de tipos**: Detecção automática e validação de tipos de dados
- **Limpeza de staging**: Remoção automática de arquivos temporários

## Estrutura de Camadas
s3://projeto-puc-fraud-prevention/
├── raw/                    # Dados brutos originais
├── raw/staging_raw/        # Área temporária (limpa a cada execução)
└── processed/              # Dados processados em Parquet

## Execução

# 1. Extrair dados
python scripts_gerais/extracao.py

# 2. Processar dados
python scripts_gerais/transformacao_carga.py
Resultados
Dados limpos, padronizados e otimizados em formato Parquet, prontos para análise exploratória e treinamento de modelos.
