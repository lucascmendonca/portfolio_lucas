Portfólio de Projetos – Lucas Cardoso Mendonça
Este repositório reúne projetos práticos nas áreas de engenharia de dados, ciência de dados, business intelligence e sistemas com IA. O objetivo é demonstrar experiência na construção de pipelines de dados, modelagem preditiva, dashboards interativos e soluções com recuperação aumentada de geração (RAG).

Projetos
1. ETL Pipeline (Engenharia de Dados)
Pasta: /etl

Pipeline de dados moderno com arquitetura em três camadas (RAW → STAGE → ANALYTICS), desenvolvido em Python com Pandas e PySpark. O projeto orquestra a ingestão, validação, deduplicação e modelagem de dados para consumo analítico.

Tecnologias: Python, Pandas, PySpark, Docker, LocalStack (simulação AWS S3/Glue)

Diferencial: Pipeline completo com testes automatizados (pytest) e ambiente isolado via Docker

2. Previsão de Inadimplência de Crédito (Ciência de Dados)
Pasta: /data-science

Projeto acadêmico que desenvolve um modelo supervisionado de machine learning para antecipar o risco de inadimplência na concessão de crédito. O objetivo é reduzir perdas financeiras, agilizar a tomada de decisão e personalizar condições de crédito.

Tecnologias: Aprendizado de máquina (modelo supervisionado)

Estrutura: Documentação completa em etapas (coleta, pré-processamento, treino, análise e otimização)

3. Dashboards em Power BI
Pasta: /power-bi

Conjunto de dashboards interativos para diferentes áreas de negócio:

Gestão de Contratos – Procurement

Gestão e Planejamento de Eventos

Dashboard de Tesouraria

Os relatórios evidenciam capacidade de transformar dados brutos em insights visuais para tomada de decisão.

4. Sistema RAG – "Cérebro Educacional" (IA & Busca Semântica)
Pasta: /rag/professor-rag

Sistema de Retrieval-Augmented Generation (RAG) que converte PDFs em uma base de conhecimento consultável via IA. O pipeline extrai texto dos documentos, gera embeddings vetoriais, armazena em banco vetorial (ChromaDB) e utiliza um LLM para responder perguntas com base no conteúdo indexado.

Tecnologias: Python, OpenAI Embeddings, OpenAI GPT, ChromaDB, PyMuPDF

Fluxo: PDF → Extração → Chunking → Embeddings → Busca semântica → LLM → Resposta

Documentos Complementares
BLUE TAG FLUXO - Performa IT.pdf – fluxograma de processo

GUIA PARA ARQUITETURA DE PASTAS SHAREPOINT (1).pdf – guia de organização de pastas

projeto_eixo_4.html – artefato HTML de projeto
