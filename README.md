mlops-news-pipeline/
├── data/
│   ├── raw/              # Store raw scraped articles
│   └── processed/        # Cleaned or tokenized versions
├── src/
│   ├── scraping/         # Your current script
│   ├── preprocessing/    # Text cleaning, deduplication
│   └── modeling/         # Future ML models (e.g., topic modeling)
├── notebooks/            # Exploratory analysis
├── dvc.yaml              # Will be added soon
├── params.yaml           # For config-driven reproducibility
├── README.md
└── requirements.txt
