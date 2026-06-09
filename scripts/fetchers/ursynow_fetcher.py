# fetchers/ursynow_fetcher.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://ursynow.um.warszawa.pl"

# Liferay AssetPublisher JSON endpoint — bypasses JS rendering
API_URL = (
    BASE_URL
    + "/api/jsonws/assetentry/get-entries"
    "?groupId=161349632"   # Ursynów site group ID
    "&classNameIds=com.liferay.journal.model.JournalArticle"
    "&start=0&end=3"
    "&_liferay_asset_publisher_INSTANCE_EobcZbNelybo_groupId=161349632"
)

def fetch_list():
    """
    Fetches 3 latest news items from Ursynów district office via Liferay API.
    Covers: local events, office announcements, infrastructure, community news.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        entries = response.json()

        results = []
        for entry in entries[:3]:
            title = entry.get("title", "").strip()
            url = BASE_URL + entry.get("url", "")
            slug = "ursynow-" + str(entry.get("entryId", ""))

            if not title or not url:
                continue

            results.append({
                "title": title,
                "url": url,
                "slug": slug,
                "tag": "乌尔西诺夫",
                "category": "Daily",
            })
        return results

    except Exception as e:
        print(f"Liferay API failed, falling back to scraper: {e}")
        return _scrape_fallback()


def _scrape_fallback():
    """Fallback HTML scraper if the API is unavailable."""
    response = requests.get(
        BASE_URL + "/aktualnosci-ursynow", timeout=10
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        title = a.get_text(strip=True)
        if "aktualnosci" in href and len(title) > 20:
            slug = "ursynow-" + href.rstrip("/").split("/")[-1][:80]
            results.append({
                "title": title,
                "url": BASE_URL + href if href.startswith("/") else href,
                "slug": slug,
                "tag": "乌尔西诺夫",
                "category": "Daily",
            })
            if len(results) >= 3:
                break
    return results


def fetch_content(url):
    """Fetches article body text."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for selector in ["div.journal-content-article", "div#content", "article", "main"]:
        el = soup.select_one(selector)
        if el:
            return el.get_text(separator=" ", strip=True)
    return ""
