import os
import yaml
import json
import newspaper
import feedparser

def scrape_news_from_feed(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        # create a newspaper article object
        article = newspaper.Article(entry.link)
        # download and parse the article
        article.download()
        article.parse()
        # extract relevant information
        articles.append({
            'title': article.title,
            'author': article.authors,
            'publish_date': article.publish_date,
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
output_dir = os.path.join('..', 'data', 'raw')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'articles.json')

# Save articles to JSON file
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Articles saved to {output_path}")