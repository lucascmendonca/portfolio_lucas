"""Engine RAG que compõe contexto e consulta um LLM para responder perguntas."""
from typing import List
import os


class RAGEngine:


    def __init__(self, embedding_service, vector_store_service, llm_model: str = "gpt-4o-mini"):
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service
        self.llm_model = llm_model
        self.openai_key = os.getenv("OPENAI_API_KEY")

    def build_context(self, query: str, top_k: int = 5) -> str:
        emb = self.embedding_service.embed_texts([query])[0]
        hits = self.vector_store_service.similarity_search(emb, top_k=top_k)
        pieces = []
        for h in hits:
            meta = h.get("metadata", {})
            title = meta.get("title") or meta.get("categoria") or h.get("id")
            pieces.append(f"[Fonte: {title}]\n{h.get('document')}\n---\n")
        return "\n".join(pieces)

    def answer(self, query: str, top_k: int = 5, max_tokens: int = 512) -> str:
        context = self.build_context(query, top_k=top_k)
        prompt = (
            "Você é um tutor pedagógico. Use o contexto abaixo para responder à pergunta de forma didática, ensinando um tópico por vez:\n\n"
            f"CONTEXT:\n{context}\nQUESTION:\n{query}\n\nResposta completa e passo a passo:")
        if not self.openai_key:
            raise RuntimeError("OPENAI_API_KEY não configurado. Não é possível chamar o LLM.")
        import openai
        openai.api_key = self.openai_key
        resp = openai.ChatCompletion.create(model=self.llm_model, messages=[{"role": "user", "content": prompt}], max_tokens=max_tokens)
        return resp["choices"][0]["message"]["content"]
