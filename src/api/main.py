from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Trendlens Lite API"}

@app.get("/articles")
def get_articles():
    with open("data/processed/articles_cleaned.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    return {"count": len(articles), "articles": articles}

from fastapi import Query

@app.get("/articles/search")
def search_articles(keyword: str = Query(...)):
    with open("data/processed/articles_cleaned.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    filtered = [a for a in articles if keyword.lower() in a["content"].lower()]
    return {"count": len(filtered), "results": filtered}

@app.get("/stats")
def get_stats():
    with open("data/processed/articles_cleaned.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    avg_length = sum(len(a["content"]) for a in articles) / len(articles)
    return {"article_count": len(articles), "avg_length": avg_length}

from fastapi import FastAPI
from collections import Counter
import re

@app.get("/trends")
def get_trends(top_n: int = 10):
    with open("data/processed/articles_cleaned.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Combine all article content
    all_text = " ".join(article["content"] for article in articles)

    # Tokenize and clean
    words = re.findall(r"\b[a-zA-Z]{4,}\b", all_text.lower())  # 4+ letter words
    stopwords = {"this", "that", "with", "from", "about", "have", "they", "will", "their", "which"}
    keywords = [word for word in words if word not in stopwords]

    # Count frequency
    freq = Counter(keywords).most_common(top_n)
    return {"top_keywords": freq}

import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import StreamingResponse

@app.get("/trends/graph")
def trends_graph(top_n: int = 10):
    with open("data/processed/articles_cleaned.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    all_text = " ".join(a["content"] for a in articles)
    words = re.findall(r"\b[a-zA-Z]{4,}\b", all_text.lower())
    stopwords = {"this", "that", "with", "from", "about", "have", "they", "will", "their", "which"}
    keywords = [w for w in words if w not in stopwords]

    freq = Counter(keywords).most_common(top_n)
    labels, counts = zip(*freq)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color="skyblue")
    plt.title("Top Trending Keywords")
    plt.xlabel("Keywords")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Stream as image
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")

# ----------------- RAG Chatbot -----------------
from pydantic import BaseModel
from functools import lru_cache

try:
    from src.rag.chatbot import RAGChatbot
except Exception:
    # Fallback for various import styles depending on working dir
    from rag.chatbot import RAGChatbot  # type: ignore


class ChatRequest(BaseModel):
    question: str


@lru_cache(maxsize=1)
def get_bot() -> RAGChatbot:
    return RAGChatbot(k=5)


@app.post("/chat")
def chat(req: ChatRequest):
    bot = get_bot()
    answer, sources = bot.ask(req.question)
    return {
        "answer": answer,
        "sources": [
            {
                "title": s.get("title"),
                "score": s.get("score"),
                "article_id": s.get("article_id"),
                "chunk_id": s.get("chunk_id"),
            }
            for s in sources
        ],
    }


@app.get("/chat")
def chat_usage():
    return {
        "message": "Use POST /chat with JSON body { 'question': '<your question>' }",
        "example": {
            "question": "What are the top topics in the articles?"
        },
        "docs": "/docs",
    }