import feedparser
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------
# Add or remove sources here. No other code changes needed.
# ---------------------------------------------------------------
RSS_SOURCES = [
    # ── English sources ──────────────────────────────────────────
    {
        "url": "https://notesfrompoland.com/feed",
        "tag": "社会",
        "category": "News",
        "slug_prefix": "nfp",
        "description": "Notes from Poland – independent English-language journalism"
    },
    {
        "url": "https://warsawinsider.pl/feed",
        "tag": "生活",
        "category": "Lifestyle",
        "slug_prefix": "wi",
        "description": "Warsaw Insider – culture, food, entertainment, travel"
    },
    {
        "url": "https://tvpworld.com/feed",
        "tag": "新闻",
        "category": "News",
        "slug_prefix": "tvp",
        "description": "TVP World – Poland's English-language state broadcaster"
    },

    # ── Polish sources — Tier 1 ──────────────────────────────────
    {
        "url": "https://www.tvn24.pl/wiadomosci-z-kraju,3.xml",
        "tag": "国内新闻",
        "category": "News",
        "slug_prefix": "tvn",
        "description": "TVN24 – Poland's leading independent TV news (domestic)"
    },
    {
        "url": "https://www.bankier.pl/rss/wiadomosci.xml",
        "tag": "经济财经",
        "category": "Economy",
        "slug_prefix": "bankier",
        "description": "Bankier.pl – finance, prices, wages, taxes"
    },
    {
        "url": "https://www.fakt.pl/rss",
        "tag": "生活资讯",
        "category": "Lifestyle",
        "slug_prefix": "fakt",
        "description": "Fakt.pl – Poland's #1 daily, everyday life and society"
    },
    {
        "url": "https://www.zw.com.pl/rss/1.html",
        "tag": "华沙生活",
        "category": "Warsaw",
        "slug_prefix": "zw",
        "description": "Życie Warszawy – Warsaw city life, transport, events"
    },

    # ── Polish sources — Tier 2 ──────────────────────────────────
    {
        "url": "https://rp.pl/rss/671-prawo",
        "tag": "法律法规",
        "category": "Law",
        "slug_prefix": "rp-prawo",
        "description": "Rzeczpospolita Prawo – law changes affecting daily life"
    },
    {
        "url": "https://rp.pl/rss/3551-zdrowie",
        "tag": "健康医疗",
        "category": "Health",
        "slug_prefix": "rp-zdrowie",
        "description": "Rzeczpospolita Zdrowie – health system, NFZ, pharmacy"
    },
    {
        "url": "https://rp.pl/rss/631-praca",
        "tag": "就业市场",
        "category": "Economy",
        "slug_prefix": "rp-praca",
        "description": "Rzeczpospolita Praca – jobs, salaries, labour law"
    },
    {
        "url": "https://www.money.pl/rss/",
        "tag": "个人理财",
        "category": "Economy",
        "slug_prefix": "money",
        "description": "Money.pl – personal finance, inflation, ZUS, taxes"
    },
]

# How many articles to fetch per source per run
ARTICLES_PER_SOURCE = 10


def fetch_list():
    results = []

    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])

            if feed.bozo:
                print(f"Warning: malformed feed at {source['url']} — skipping.")
                continue

            for entry in feed.entries[:ARTICLES_PER_SOURCE]:
                raw_slug = entry.get("link", "").rstrip("/").split("/")[-1]
                if not raw_slug:
                    continue

                slug = f"{source['slug_prefix']}-{raw_slug}"[:200]

                results.append({
                    "title": entry.get("title", "").strip(),
                    "url": entry.get("link", "").strip(),
                    "slug": slug,
                    "tag": source["tag"],
                    "category": source["category"],
                })

        except Exception as e:
            print(f"Failed to fetch RSS from {source['url']}: {e} — skipping.")
            continue

    return results


def fetch_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in ["article", "main", "body"]:
            element = soup.find(tag)
            if element:
                return element.get_text(separator=" ", strip=True)

        return ""

    except Exception as e:
        print(f"Failed to fetch content from {url}: {e}")
        return ""
        
