import os
import yaml
import json
import newspaper
import feedparser
from datetime import datetime


def scrape_news_from_feed(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        article = newspaper.Article(entry.link)
        try:
            article.download()
            article.parse()
        except Exception as e:
            print(f"Failed to process {entry.link}: {e}")
            continue

        publish_date = article.publish_date
        if isinstance(publish_date, datetime):
            publish_date = publish_date.isoformat()  # Converts to 'YYYY-MM-DDTHH:MM:SS'

        articles.append({
            'source': url,
            'title': article.title,
            'author': article.authors,
            'publish_date': publish_date,
            'content': article.text
        })
    return articles

with open("params.yaml") as f:
    params = yaml.safe_load(f)

feed_urls = params["scraping"]["feed_urls"]
all_articles = []

for url in feed_urls:
    articles = scrape_news_from_feed(url)
    all_articles.extend(articles)


# # print the extracted articles
# for article in articles:
#     print('Title:', article['title'])
#     print('Author:', article['author'])
#     print('Publish Date:', article['publish_date'])
#     print('Content:', article['content'])
#     print()


# Ensure the output directory exists
output_dir = os.path.join('data', 'raw')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'articles.json')
print(f"Scraped {len(all_articles)} articles from {len(feed_urls)} feeds.")

metrics = {
    "scraping": {
        "article_count": len(all_articles),
        "feed_count": len(feed_urls),
        "avg_length": sum(len(a['content']) for a in all_articles) / len(all_articles)
    }
}

with open("metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

# Save articles to JSON file
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print(f"Articles saved to {output_path}")