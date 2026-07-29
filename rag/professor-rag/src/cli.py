"""Pontos de entrada CLI para construir o pipeline RAG pedagógico."""
import argparse
from pathlib import Path

from cerebro import PDFProcessor, ChunkProcessor, EmbeddingService, VectorStoreService, RAGEngine


def build_pipeline(pdf_paths, persist_dir=None):
    pdf = PDFProcessor()
    chunker = ChunkProcessor()
    embed = EmbeddingService()
    vstore = VectorStoreService(persist_directory=persist_dir)

    doc_ids = []
    docs = []
    metadatas = []
    texts = []

    for p in pdf_paths:
        path = Path(p)
        txt = pdf.extract_text(str(path))
        h = __import__('hashlib').sha256(txt.encode('utf-8')).hexdigest()
        chunks = chunker.split_text(txt)
        for i, c in enumerate(chunks):
            doc_id = f"{path.stem}-{i}-{h[:8]}"
            doc_ids.append(doc_id)
            docs.append(c)
            metadatas.append({"source": str(path), "title": path.stem})
            texts.append(c)

    embeddings = embed.embed_texts(texts)
    vstore.upsert(ids=doc_ids, embeddings=embeddings, metadatas=metadatas, documents=docs)
    print(f"Inseridos {len(doc_ids)} fragmentos na base vetorial.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pipeline RAG Pedagógico (não executa por padrão).')
    parser.add_argument('--pdf', nargs='+', help='PDFs para processar', required=False)
    parser.add_argument('--persist-dir', help='Diretório de persistência do chroma', default=None)
    args = parser.parse_args()
    if args.pdf:
        build_pipeline(args.pdf, persist_dir=args.persist_dir)
    else:
        print('Nenhum PDF fornecido. Execução cancelada.')
