import feedparser
import json
from datetime import datetime

# RSSフィードURLリスト
RSS_URLS = [
    "https://www.nhk.or.jp/rss/news/cat0.xml",
    "https://www.nhk.or.jp/rss/news/cat1.xml"
]

# JSONファイル出力先
OUTPUT_FILE = "rss_data.json"

def fetch_rss():
    all_posts = []
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            all_posts.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "summary": entry.summary if hasattr(entry, "summary") else "",
            })
    
    # 重複排除（タイトルを基準）
    unique_posts = {post["title"]: post for post in all_posts}.values()

    # 投稿日時で降順ソート
    sorted_posts = sorted(unique_posts, key=lambda x: datetime.strptime(x["published"], "%a, %d %b %Y %H:%M:%S %Z"), reverse=True)

    # トップ10を取得
    return sorted_posts[:10]

if __name__ == "__main__":
    posts = fetch_rss()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
