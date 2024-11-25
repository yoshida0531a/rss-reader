const RSS_URLS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", // サンプルRSSフィード
    "https://example.com/rss" // 他のRSSフィードを追加可能
];

async function fetchRSS() {
    let allPosts = [];
    for (let url of RSS_URLS) {
        try {
            const response = await fetch(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(url)}`);
            const data = await response.json();
            allPosts = allPosts.concat(data.items);
        } catch (error) {
            console.error(`Error fetching RSS feed: ${url}`, error);
        }
    }

    // 重複を削除
    const uniquePosts = allPosts.filter((post, index, self) =>
        index === self.findIndex((t) => t.title === post.title)
    );

    // 投稿日で降順ソート
    const sortedPosts = uniquePosts.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));

    // トップ10を取得
    return sortedPosts.slice(0, 10);
}

function displayRSS(posts) {
    const feedList = document.getElementById("feed-list");
    feedList.innerHTML = ""; // リストをクリア
    posts.forEach(post => {
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <a href="${post.link}" target="_blank">${post.title}</a>
            <p>${new Date(post.pubDate).toLocaleString()}</p>
        `;
        feedList.appendChild(listItem);
    });
}

// 初期化
async function init() {
    const posts = await fetchRSS();
    displayRSS(posts);
}

init();
