import feedparser

# サンプルRSSフィードURL
RSS_URL = "https://example.com/rss"

# フィードを取得
def fetch_rss(url):
    feed = feedparser.parse(url)
    for entry in feed.entries:
        print(f"Title: {entry.title}")
        print(f"Link: {entry.link}")
        print(f"Published: {entry.published}\n")

if __name__ == "__main__":
    fetch_rss(RSS_URL)
