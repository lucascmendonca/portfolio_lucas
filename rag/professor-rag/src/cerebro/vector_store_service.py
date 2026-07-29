"""Adaptador do ChromaDB para operações de armazenamento vetorial."""
from typing import List, Optional
import os


class VectorStoreService:

    def __init__(self, persist_directory: Optional[str] = None, collection_name: str = "colecao_pedagogica"):
        try:
            import chromadb
            from chromadb.config import Settings
            self.chromadb = chromadb
        except Exception:
            raise RuntimeError("chromadb está ausente. Instale chromadb para usar o VectorStoreService.")

        persist_directory = persist_directory or os.getenv("CHROMA_PERSIST_DIR") or "./chroma_db"
        settings = Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_directory)
        self.client = chromadb.Client(settings=settings)
        self.collection = self._get_or_create_collection(collection_name)

    def _get_or_create_collection(self, name: str):
        try:
            return self.client.get_collection(name)
        except Exception:
            return self.client.create_collection(name)

    def upsert(self, ids: List[str], embeddings: List[List[float]], metadatas: List[dict], documents: List[str]):
        self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

    def similarity_search(self, embedding: List[float], top_k: int = 5):
        res = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        # retorna lista de (id, documento, metadados, score)
        results = []
        for i in range(len(res["ids"][0])):
            results.append({
                "id": res["ids"][0][i],
                "document": res["documents"][0][i],
                "metadata": res["metadatas"][0][i],
                "score": res["distances"][0][i] if "distances" in res else None,
            })
        return results
