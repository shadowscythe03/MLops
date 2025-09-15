# 📰 MLops News Scraping Pipeline

This project builds a reproducible, modular pipeline for scraping news articles from RSS feeds, tracking data and experiments with DVC and MLflow, and preparing for deployment via FastAPI.

---

## 📁 Project Structure

MLops/
├── data/
│   ├── raw/              # Scraped articles
│   └── processed/        # Cleaned or tokenized data
├── src/
│   ├── scraping/         # RSS feed scraping logic
│   ├── preprocessing/    # Text cleaning (coming soon)
├── notebooks/            # Exploratory analysis
├── dvc.yaml              # Pipeline definition
├── params.yaml           # Configurable feed URLs
├── environment.yml       # Conda environment
└── README.md

---

## 🚀 Pipeline Overview

### ✅ Stage 1: Scraping

- Parses multiple RSS feeds using `feedparser`
- Downloads and extracts article content via `newspaper3k`
- Output saved to `data/raw/articles.json`

### 🔁 Stage 2: Preprocessing *(coming soon)*

- Deduplication, tokenization, and cleaning
- Output to `data/processed/articles_cleaned.json`

### 📊 Experiment Tracking

- MLflow logs feed source, article count, and metadata
- Future integration with topic modeling and summarization

### 🌐 Deployment

- FastAPI service to expose scraping and summaries via REST API

---

<!-- ## ⚙️ Setup Instructions

# Clone the repo
git clone https://github.com/shadowscythe03/MLops.git
cd MLops

# Create environment
conda env create -f environment.yml
conda activate mlops

# Reproduce pipeline
dvc repro -->

<!-- 📌 Configuration
Edit params.yaml to change feed sources:
scraping:
  feed_urls:
    - https://feeds.bbci.co.uk/news/rss.xml
    - https://www.reuters.com/rssFeed/topNews -->

📈 Metrics & Logging
Coming soon:

- Article count
- Average length
- Source distribution

🛠️ To Do

- [X] Scraping pipeline with DVC
- [ ] Preprocessing stage
- [ ] MLflow metrics logging
- [ ] FastAPI deployment
- [ ] Dockerization

<!-- 🤝 Contributing
Pull requests welcome! Please follow modular structure and document any new stages in dvc.yaml. -->
