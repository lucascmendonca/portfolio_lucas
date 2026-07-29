"""Cria chunks com outputs longos preferencialmente usando langchain"""
from typing import List


class ChunkProcessor:

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            self._splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size, chunk_overlap=self.overlap
            )
            self._use_langchain = True
        except Exception:
            self._splitter = None
            self._use_langchain = False

    def split_text(self, text: str) -> List[str]:
        if self._use_langchain and self._splitter is not None:
            return self._splitter.split_text(text)
        # Divisor alternativo simples: dividir por parágrafos e gerar janelas
        paras = [p.strip() for p in text.split('\n') if p.strip()]
        chunks = []
        current = ""
        for p in paras:
            if len(current) + len(p) + 1 <= self.chunk_size:
                current = (current + "\n" + p).strip()
            else:
                if current:
                    chunks.append(current)
                if len(p) > self.chunk_size:
                    # hard-split long paragraph
                    for i in range(0, len(p), self.chunk_size - self.overlap):
                        chunks.append(p[i:i + self.chunk_size])
                    current = ""
                else:
                    current = p
        if current:
            chunks.append(current)
        return chunks
