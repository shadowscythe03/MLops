# Lightweight CPU image for FastAPI + Transformers
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HUB_DISABLE_TELEMETRY=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy manifests first for caching
COPY environment.yml /app/environment.yml

# Install pip dependencies (avoid conda for smaller image)
# We will manually install runtime deps that we need from environment.yml
RUN pip install --upgrade pip && \
    pip install fastapi uvicorn[standard] pytest matplotlib \
                transformers sentence-transformers faiss-cpu huggingface-hub torch dvc

# Copy source
COPY src /app/src
COPY data/processed /app/data/processed

# Build RAG index at build time if not present (optional)
RUN python -m src.rag.build_index || true

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
