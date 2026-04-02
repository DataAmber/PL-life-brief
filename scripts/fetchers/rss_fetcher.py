import feedparser
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------
# Add or remove sources here. No other code changes needed.
# ---------------------------------------------------------------
RSS_SOURCES = [
    {
        "url": "https://notesfrompoland.com/feed",
        "tag": "Society",
        "category": "Daily",
        "slug_prefix": "nfp",
        "description": "Notes from Poland – independent English-language journalism"
    },
    {
        "url": "https://warsawinsider.pl/feed",
        "tag": "Lifestyle",
        "category": "Daily",
        "slug_prefix": "wi",
        "description": "Warsaw Insider – culture, food, entertainment, travel"
    },
    {
        "url": "https://tvpworld.com/feed",
        "tag": "News",
        "category": "Daily",
        "slug_prefix": "tvp",
        "description": "TVP World – Poland's English-language state broadcaster"
    },
]

# How many articles to fetch per source per run
ARTICLES_PER_SOURCE = 3


def fetch_list():
    """
    Iterates all RSS_SOURCES and returns a flat list of article metadata dicts,
    up to ARTICLES_PER_SOURCE items per source.
    Compatible with engine.py's expected item format.
    """
    results = []

    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])

            if feed.bozo:
                # bozo=True means feedparser encountered a malformed feed
                print(f"Warning: malformed feed at {source['url']} — skipping.")
                continue

            for entry in feed.entries[:ARTICLES_PER_SOURCE]:
                # Build a slug from the URL path, prefixed to avoid collisions
                raw_slug = entry.get("link", "").rstrip("/").split("/")[-1]
                if not raw_slug:
                    continue

                slug = f"{source['slug_prefix']}-{raw_slug}"[:200]  # keep under key limit

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
    """
    Fetches the full article text from a given URL.
    Tries <article> tag first, falls back to <main>, then <body>.
    """
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

