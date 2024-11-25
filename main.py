from flask import Flask, render_template
import feedparser
import schedule
import time
from bs4 import BeautifulSoup
from threading import Thread

app = Flask(__name__)

# サンプルRSSフィードURLリスト
RSS_URLS = [
    "https://example.com/rss1",
    "https://example.com/rss2",
]

# グローバル変数に最新フィードを保存
latest_posts = []

# 重複を削除する関数
def remove_duplicates(entries):
    seen_titles = set()
    unique_entries = []
    for entry in entries:
        title = entry.title.lower()
        if title not in seen_titles:
            seen_titles.add(title)
            unique_entries.append(entry)
    return unique_entries

# フィードを取得して更新
def update_rss():
    global latest_posts
    all_entries = []
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        all_entries.extend(feed.entries)
    
    # 重複削除
    unique_entries = remove_duplicates(all_entries)
    
    # ソート（ここでは投稿日順を例に降順）
    sorted_entries = sorted(unique_entries, key=lambda x: x.published_parsed, reverse=True)
    
    # トップ10のみ取得
    latest_posts = sorted_entries[:10]

# サーバー起動時にRSSを初期化
update_rss()

# スケジュールで6時間ごとにRSSを更新
def schedule_updates():
    schedule.every(6).hours.do(update_rss)
    while True:
        schedule.run_pending()
        time.sleep(1)

# スケジュールを別スレッドで実行
thread = Thread(target=schedule_updates)
thread.daemon = True
thread.start()

@app.route("/")
def index():
    global latest_posts
    return render_template("index.html", posts=latest_posts)

if __name__ == "__main__":
    app.run(debug=True)
