from flask import Flask, render_template
import feedparser

app = Flask(__name__)

@app.route("/")
def index():
    RSS_URL = "https://www.nhk.or.jp/rss/news/cat0.xml"
    feed = feedparser.parse(RSS_URL)
    return render_template("index.html", entries=feed.entries)

if __name__ == "__main__":
    app.run(debug=True)
