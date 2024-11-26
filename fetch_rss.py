from datetime import datetime
import feedparser
import json  # JSONモジュールを追加

# RSSフィードのURLリスト
RSS_FEEDS = [
    "https://www.nhk.or.jp/rss/news/cat0.xml",
    "https://www.nhk.or.jp/rss/news/cat1.xml",
]

def fetch_rss():
    posts = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            posts.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
            })

    # 重複を排除
    unique_posts = {post["title"]: post for post in posts}.values()

    # 日時をパースする関数
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            print(f"Failed to parse date: {date_str}")
            return datetime.min

    # ソート（最新順）
    sorted_posts = sorted(unique_posts, key=lambda x: parse_date(x["published"]), reverse=True)

    # 上位10件のみ取得
    return sorted_posts[:10]

if __name__ == "__main__":
    posts = fetch_rss()

    # JSONファイルに保存
    with open("rss_data.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

    print("rss_data.json が生成されました。")
