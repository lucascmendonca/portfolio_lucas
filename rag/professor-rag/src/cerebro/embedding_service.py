"""Abstração de serviço de embeddings. Suporta embeddings OpenAI por padrão."""
from typing import List
import os


class EmbeddingService:
    

    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            # allow initialization but calls will fail with clear message
            self._available = False
        else:
            self._available = True
            try:
                import openai
                openai.api_key = self.openai_api_key
                self._client = openai
            except Exception:
                self._available = False

    def embed_texts(self, texts: List[str]) -> List[List[float]]:

        if not self._available:
            raise RuntimeError("OpenAI API key not configured. Set OPENAI_API_KEY in environment.")
        # Use batch embedding
        resp = self._client.Embeddings.create(input=texts, model=self.model)
        return [r["embedding"] for r in resp["data"]]
