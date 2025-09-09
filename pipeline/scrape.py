import argparse
import os
import pandas as pd
from newspaper import Article
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_moneycontrol(topic, limit=10):
    base_url = f"https://www.moneycontrol.com/news/search/?query={topic.replace(' ', '%20')}"
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = []
    for card in soup.select("li.clearfix")[:limit]:
        headline = card.find("h2")
        url = card.find("a")["href"] if card.find("a") else None
        summary = card.find("p").text if card.find("p") else ""
        articles.append({"headline": headline.text.strip() if headline else "",
                         "url": url, "summary": summary})
    return articles

def scrape_reuters(topic, limit=10):
    base_url = f"https://www.reuters.com/site-search/?query={topic.replace(' ', '+')}"
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = []
    for card in soup.select(".search-result-content")[:limit]:
        headline = card.find("h3")
        url = "https://www.reuters.com" + card.find("a")["href"] if card.find("a") else None
        summary = card.find("p").text if card.find("p") else ""
        articles.append({"headline": headline.text.strip() if headline else "",
                         "url": url, "summary": summary})
    return articles

def scrape_newspaper3k(urls):
    articles = []
    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            articles.append({
                "headline": article.title,
                "url": url,
                "summary": article.text
            })
        except Exception as e:
            continue
    return articles

def main(topic, outdir, limit):
    os.makedirs(outdir, exist_ok=True)
    all_articles = []
    # MoneyControl
    all_articles += scrape_moneycontrol(topic, limit=limit//3)
    # Reuters
    all_articles += scrape_reuters(topic, limit=limit//3)
    # NDTV (exercise: add NDTV scraper if desired)
    # If you want to extract full text, use Newspaper3k:
    urls = [a["url"] for a in all_articles if a["url"]]
    full_articles = scrape_newspaper3k(urls)
    df = pd.DataFrame(full_articles)
    fname = os.path.join(outdir, f"{topic.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
    df.to_csv(fname, index=False)
    print(f"Saved {len(df)} articles to {fname}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", "-t", required=True)
    ap.add_argument("--outdir", default="data/raw")
    ap.add_argument("--limit", type=int, default=12)
    args = ap.parse_args()
    main(args.topic, args.outdir, args.limit)