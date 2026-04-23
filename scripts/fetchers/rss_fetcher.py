import feedparser
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------
# Add or remove sources here. No other code changes needed.
# ---------------------------------------------------------------
RSS_SOURCES = [
    # ── English news ─────────────────────────────────────────────
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
        "url": "https://kidsinthecity.pl/feed",
        "tag": "活动资讯",
        "category": "Events",
        "slug_prefix": "kitc",
        "description": "Kids in the City – family events, festivals, exhibitions in Warsaw"
    },

    # ── Polish news ───────────────────────────────────────────────
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
        "url": "https://www.money.pl/rss/",
        "tag": "个人理财",
        "category": "Economy",
        "slug_prefix": "money",
        "description": "Money.pl – personal finance, inflation, ZUS, taxes"
    },

    # ── Analysis & commentary ─────────────────────────────────────
    {
        "url": "https://expatinpoland.pl/feed",
        "tag": "移民解读",
        "category": "Analysis",
        "slug_prefix": "eip",
        "description": "Expat in Poland – practical expat life advice and commentary"
    },
    {
        "url": "https://polandunraveled.com/feed",
        "tag": "波兰解读",
        "category": "Analysis",
        "slug_prefix": "pur",
        "description": "Poland Unraveled – expat guide, culture, practical Poland info"
    },
    {
        "url": "https://euractiv.com/?feed=mcfeed",
        "tag": "欧盟政策",
        "category": "Analysis",
        "slug_prefix": "euractiv",
        "description": "Euractiv – EU affairs and policy analysis relevant to Poland"
    },

    # ── Transport alerts ──────────────────────────────────────────
    {
        "url": "https://www.wtp.waw.pl/zmiany/feed/",
        "tag": "交通变化",
        "category": "Warsaw",
        "slug_prefix": "wtp-zmiany",
        "description": "WTP Warsaw – planned route changes"
    },
    {
        "url": "https://www.wtp.waw.pl/utrudnienia/feed/",
        "tag": "交通警报",
        "category": "Warsaw",
        "slug_prefix": "wtp-alert",
        "description": "WTP Warsaw – live service disruptions"
    },
        {
        "url": "https://rp.pl/rss/671-prawo",
        "tag": "税务”,
        "category": "Warsaw",
        "slug_prefix": "rpplt",
        "description": "WTP Warsaw – live service disruptions"
    },


    # ── Removed (confirmed broken feeds) ─────────────────────────
    # https://tvpworld.com/feed         — malformed
    # https://www.zw.com.pl/rss/1.html  — malformed
    # https://rp.pl/rss/671-prawo       — malformed
    # https://rp.pl/rss/3551-zdrowie    — malformed
    # https://rp.pl/rss/631-praca       — malformed
    # https://visegradinsight.eu/feed/  — paywalled
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
                raw_slug = raw_slug.split("?")[0]
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
        
