import os
import json
from typing import List, Dict, Tuple

import numpy as np

try:
    import faiss  # type: ignore
    _HAS_FAISS = True
except Exception:
    faiss = None  # type: ignore
    _HAS_FAISS = False

from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


INDEX_DIR = os.path.join("data", "processed", "index")
EMBEDDINGS_FILE = os.path.join(INDEX_DIR, "embeddings.faiss")
EMBEDDINGS_NPY = os.path.join(INDEX_DIR, "embeddings.npy")
METADATA_FILE = os.path.join(INDEX_DIR, "metadata.jsonl")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
GEN_MODEL = os.getenv("GEN_MODEL", "google/flan-t5-small")


class RAGChatbot:
    def __init__(self, k: int = 5):
        if not (os.path.exists(EMBEDDINGS_FILE) or os.path.exists(EMBEDDINGS_NPY)) or not os.path.exists(METADATA_FILE):
            raise FileNotFoundError("RAG index not found. Run src/rag/build_index.py first.")

        # Load vector index
        self.index = None
        self.embeddings = None
        if _HAS_FAISS and os.path.exists(EMBEDDINGS_FILE):
            self.index = faiss.read_index(EMBEDDINGS_FILE)
        else:
            # numpy fallback
            self.embeddings = np.load(EMBEDDINGS_NPY).astype("float32")

        # Load metadata and corpus texts
        self.corpus: List[Dict] = []
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                self.corpus.append(json.loads(line))

        # Embedding model
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

        # Generation model
        self.tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
        self.generator = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL)

        self.k = k

    def retrieve(self, query: str, k: int | None = None) -> List[Dict]:
        k = k or self.k
        q_vec = self.embedder.encode([query], normalize_embeddings=True)
        q_vec = np.asarray(q_vec, dtype="float32")

        results = []
        if self.index is not None:
            scores, idxs = self.index.search(q_vec, k)
            for score, idx in zip(scores[0], idxs[0]):
                if idx == -1:
                    continue
                doc = self.corpus[int(idx)]
                results.append({"score": float(score), **doc})
        else:
            # brute-force cosine similarity on CPU
            sims = (self.embeddings @ q_vec[0])  # embeddings are already normalized
            topk_idx = np.argsort(-sims)[:k]
            for idx in topk_idx:
                doc = self.corpus[int(idx)]
                results.append({"score": float(sims[int(idx)]), **doc})
        return results

    def generate(self, query: str, contexts: List[str]) -> str:
        # Build a concise prompt for flan-t5
        context_text = "\n\n".join(contexts)
        prompt = (
            "Answer the question using only the context. If unsure, say you don't know.\n"
            f"Context:\n{context_text}\n\n"
            f"Question: {query}\n"
            "Answer:"
        )
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        outputs = self.generator.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            num_beams=4,
            length_penalty=0.9,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    def ask(self, query: str) -> Tuple[str, List[Dict]]:
        hits = self.retrieve(query)
        contexts = [h["text"] for h in hits]
        answer = self.generate(query, contexts)
        return answer, hits
