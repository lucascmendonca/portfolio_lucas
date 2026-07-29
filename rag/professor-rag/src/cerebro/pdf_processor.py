"""Utilitários de extração de texto de PDF e hashing de arquivos."""
import hashlib
from typing import Tuple


class PDFProcessor:
    

    def __init__(self):
        try:
            import fitz  # PyMuPDF
            self._has_fitz = True
        except Exception:
            self._has_fitz = False

    def extract_text(self, path: str) -> str:

        if self._has_fitz:
            import fitz
            doc = fitz.open(path)
            parts = []
            for page in doc:
                parts.append(page.get_text())
            return "\n".join(parts)
        else:
            # Alternativa: tentar pypdf via interface similar ao PyPDF2
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(path)
                texts = []
                for p in reader.pages:
                    texts.append(p.extract_text() or "")
                return "\n".join(texts)
            except Exception as e:
                raise RuntimeError("Nenhuma biblioteca de PDF instalada (pymupdf ou PyPDF2).")


def file_hash(path: str) -> str:

    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
