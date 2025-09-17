import os
import json
from typing import List, Dict

import numpy as np

try:
    import faiss  # type: ignore
    _HAS_FAISS = True
except Exception:
    faiss = None  # type: ignore
    _HAS_FAISS = False

from sentence_transformers import SentenceTransformer


DATA_PATH = os.path.join("data", "processed", "articles_cleaned.json")
INDEX_DIR = os.path.join("data", "processed", "index")
EMBEDDINGS_FILE = os.path.join(INDEX_DIR, "embeddings.faiss")
EMBEDDINGS_NPY = os.path.join(INDEX_DIR, "embeddings.npy")
METADATA_FILE = os.path.join(INDEX_DIR, "metadata.jsonl")
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


def chunk_text(text: str, max_chars: int = 800, overlap: int = 100) -> List[str]:
    # Simple char-based chunker suitable for small CPU workloads
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


def load_articles() -> List[Dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build() -> None:
    os.makedirs(INDEX_DIR, exist_ok=True)

    articles = load_articles()
    model = SentenceTransformer(MODEL_NAME)

    texts: List[str] = []
    metadata: List[Dict] = []

    for idx, art in enumerate(articles):
        content = art.get("content", "")
        title = art.get("title", "")
        for chunk_id, chunk in enumerate(chunk_text(content)):
            chunk_text_full = f"{title}\n\n{chunk}".strip()
            texts.append(chunk_text_full)
            metadata.append({
                "article_id": idx,
                "chunk_id": chunk_id,
                "title": title,
            })

    # Compute embeddings
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.asarray(embeddings, dtype="float32")

    # Save numpy embeddings for universal fallback
    np.save(EMBEDDINGS_NPY, embeddings)

    # FAISS index (cosine via inner product with normalized vectors)
    if _HAS_FAISS:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        # Save index
        faiss.write_index(index, EMBEDDINGS_FILE)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        for md, text in zip(metadata, texts):
            f.write(json.dumps({**md, "text": text}, ensure_ascii=False) + "\n")

    if _HAS_FAISS:
        print(f"Index built with {len(texts)} chunks -> {EMBEDDINGS_FILE} and {EMBEDDINGS_NPY}")
    else:
        print(f"Index built with {len(texts)} chunks (FAISS unavailable). Using numpy fallback -> {EMBEDDINGS_NPY}")


if __name__ == "__main__":
    build()
