
## Objetivo

O Cérebro Educacional é um sistema RAG (*Retrieval-Augmented Generation*) que transforma PDFs em uma base de conhecimento consultável por Inteligência Artificial.

O sistema extrai informações dos documentos, gera embeddings vetoriais e utiliza um LLM para responder perguntas com base no conteúdo indexado.

---

# Arquitetura

```text
PDFs
 │
 ▼
Extração de Texto
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
ChromaDB
 │
 ▼
Busca Semântica
 │
 ▼
LLM
 │
 ▼
Resposta
```

---

# Estrutura do Código

```text
src/
│
├── cli.py
│
└── cerebro/
    ├── pdf_processor.py
    ├── chunk_processor.py
    ├── embedding_service.py
    ├── vector_store_service.py
    └── rag_engine.py
```

---

# Componentes

## PDFProcessor

Arquivo:

```python
pdf_processor.py
```

Responsável por:

* Ler arquivos PDF
* Extrair texto
* Validar documentos

Fluxo:

```text
PDF → Texto
```

---

## ChunkProcessor

Arquivo:

```python
chunk_processor.py
```

Responsável por:

* Dividir textos longos em partes menores
* Criar sobreposição entre chunks

Fluxo:

```text
Texto → Chunks
```

Exemplo:

```text
Capítulo Completo
      ↓
Chunk 1
Chunk 2
Chunk 3
```

---

## EmbeddingService

Arquivo:

```python
embedding_service.py
```

Responsável por:

* Converter texto em vetores numéricos
* Utilizar a API de Embeddings da OpenAI

Fluxo:

```text
Chunk → Embedding
```

---

## VectorStoreService

Arquivo:

```python
vector_store_service.py
```

Responsável por:

* Armazenar embeddings
* Realizar buscas por similaridade

Banco utilizado:

```text
ChromaDB
```

Fluxo:

```text
Embedding → Banco Vetorial
```

---

## RAGEngine

Arquivo:

```python
rag_engine.py
```

Responsável por:

* Receber perguntas
* Buscar conteúdo relevante
* Montar contexto
* Consultar o LLM
* Gerar respostas

Fluxo:

```text
Pergunta
   ↓
Busca Vetorial
   ↓
Contexto
   ↓
GPT
   ↓
Resposta
```

---

# Pipeline de Indexação

## 1. Leitura

```text
PDF → Texto
```

## 2. Fragmentação

```text
Texto → Chunks
```

## 3. Vetorização

```text
Chunks → Embeddings
```

## 4. Armazenamento

```text
Embeddings → ChromaDB
```

---

# Pipeline de Consulta

## 1. Usuário faz uma pergunta

```text
"O que é um loop for?"
```

## 2. Pergunta é convertida em embedding

```text
Pergunta → Vetor
```

## 3. Busca semântica

```text
Vetor → ChromaDB
```

## 4. Recuperação dos melhores trechos

```text
Top-K Chunks
```

## 5. Construção do contexto

```text
Chunks → Contexto
```

## 6. Consulta ao LLM

```text
Contexto + Pergunta
```

## 7. Resposta final

```text
Resposta didática
```

---

# Resumo do Fluxo Completo

```text
PDF
 │
 ▼
PDFProcessor
 │
 ▼
ChunkProcessor
 │
 ▼
EmbeddingService
 │
 ▼
VectorStoreService
 │
 ▼
ChromaDB
 │
 ├─────────────► Consulta
 │                    │
 ▼                    ▼
RAGEngine ◄── Pergunta do Usuário
 │
 ▼
LLM
 │
 ▼
Resposta
```

## Tecnologias Utilizadas

* Python
* OpenAI Embeddings
* OpenAI GPT
* ChromaDB
* PyMuPDF
* LangChain (opcional)

## Resultado

O sistema transforma materiais educacionais em uma base de conhecimento inteligente capaz de responder perguntas utilizando o conteúdo dos documentos previamente indexados.
