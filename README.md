# Portfólio de Dados, Analytics e Inteligência Artificial

Este repositório reúne projetos práticos nas áreas de **Engenharia de Dados**, **Ciência de Dados**, **Business Intelligence** e **Sistemas de Inteligência Artificial**. O objetivo é demonstrar experiência na construção de pipelines de dados, modelagem preditiva, dashboards interativos e soluções baseadas em **Retrieval-Augmented Generation (RAG)**.

---

# Projetos

## 1. ETL Pipeline (Engenharia de Dados)

**Pasta:** `/etl`

Pipeline de dados moderno com arquitetura em três camadas (**RAW → STAGE → ANALYTICS**), desenvolvido em Python utilizando Pandas e PySpark. O projeto realiza ingestão, validação, deduplicação e modelagem de dados para consumo analítico.

### Tecnologias
- Python
- Pandas
- PySpark
- Docker
- LocalStack (simulação de serviços AWS como S3 e Glue)

### Diferenciais
- Pipeline completo de ponta a ponta
- Testes automatizados com `pytest`
- Ambiente isolado e reproduzível via Docker
- Estrutura baseada em boas práticas de Engenharia de Dados

---

## 2. Previsão de Inadimplência de Crédito (Ciência de Dados)

**Pasta:** `/data-science`

Projeto acadêmico focado no desenvolvimento de um modelo supervisionado de Machine Learning para prever o risco de inadimplência em operações de crédito.

O objetivo é auxiliar instituições financeiras na redução de perdas, melhoria da tomada de decisão e personalização das condições de crédito.

### Tecnologias
- Python
- Machine Learning Supervisionado
- Análise Estatística

### Estrutura do Projeto
1. Coleta de dados
2. Pré-processamento
3. Engenharia de atributos
4. Treinamento do modelo
5. Avaliação de desempenho
6. Otimização e ajustes

### Objetivos de Negócio
- Redução de riscos financeiros
- Aumento da assertividade na concessão de crédito
- Apoio à tomada de decisão baseada em dados

---

## 3. Dashboards em Power BI

**Pasta:** `/power-bi`

Coleção de dashboards interativos desenvolvidos para diferentes áreas de negócio, com foco em visualização de dados, monitoramento de indicadores e suporte à tomada de decisão.

### Projetos Disponíveis

#### Gestão de Contratos – Procurement
Dashboard voltado ao acompanhamento de contratos, vencimentos, fornecedores e indicadores de desempenho.

#### Gestão e Planejamento de Eventos
Painel para monitoramento de eventos, recursos, cronogramas e métricas operacionais.

#### Dashboard de Tesouraria
Visualização financeira para acompanhamento de fluxo de caixa, pagamentos, recebimentos e indicadores financeiros.

### Competências Demonstradas
- Modelagem de dados
- Criação de métricas com DAX
- Storytelling com dados
- Desenvolvimento de dashboards executivos
- Transformação de dados em insights acionáveis

---

## 4. Sistema RAG – "Cérebro Educacional" (IA & Busca Semântica)

**Pasta:** `/rag/professor-rag`

Sistema baseado em **Retrieval-Augmented Generation (RAG)** que transforma documentos PDF em uma base de conhecimento consultável por Inteligência Artificial.

O pipeline realiza a extração de texto dos documentos, geração de embeddings vetoriais, armazenamento em banco vetorial e recuperação contextual para responder perguntas utilizando modelos de linguagem (LLMs).

### Tecnologias
- Python
- OpenAI Embeddings
- OpenAI GPT
- ChromaDB
- PyMuPDF

### Fluxo da Solução

```text
PDF
 ↓
Extração de Texto
 ↓
Chunking
 ↓
Geração de Embeddings
 ↓
Armazenamento Vetorial (ChromaDB)
 ↓
Busca Semântica
 ↓
LLM (GPT)
 ↓
Resposta Contextualizada
