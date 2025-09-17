import os
import json
import re
from unidecode import unidecode


def clean_text(text):
    # Basic cleaning: remove extra whitespace, HTML tags, and replaces non-ASCII with ASCII
    text = unidecode(text)
    text = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags
    text = re.sub(r"\s+", " ", text)     # Collapse whitespace
    text = text.encode("ascii", "ignore").decode()  # Remove non-ASCII
    return text.strip()


def main():
    # Load raw articles
    with open("data/raw/articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Apply cleaning
    cleaned_articles = []
    for article in articles:
        cleaned = {
            "title": clean_text(article["title"]),
            "author": article["author"],
            "publish_date": article["publish_date"],
            "content": clean_text(article["content"])
        }
        cleaned_articles.append(cleaned)

    # Save cleaned output
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/articles_cleaned.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_articles, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(cleaned_articles)} cleaned articles to data/processed/articles_cleaned.json")


if __name__ == "__main__":
    main()