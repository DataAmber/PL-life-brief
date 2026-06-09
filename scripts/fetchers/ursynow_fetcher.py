import requests
from bs4 import BeautifulSoup

BASE_URL = "https://ursynow.um.warszawa.pl"
LIST_URL = BASE_URL + "/aktualnosci-ursynow"

# Mimic a real browser to avoid 403 blocks
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pl-PL,pl;q=0.9",
}


def fetch_list():
    """
    Fetches 3 latest news items from Ursynów district office.
    Covers: local events, office announcements, infrastructure, community news.
    """
    try:
        response = requests.get(LIST_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        # Liferay renders article links with long descriptive hrefs
        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            title = a.get_text(strip=True)

            # Filter: must be an article link with a meaningful title
            if (
                "aktualnosci" in href
                and len(title) > 20
                and href != LIST_URL
                and not href.endswith("aktualnosci-ursynow")
            ):
                full_url = BASE_URL + href if href.startswith("/") else href
                slug = "ursynow-" + href.rstrip("/").split("/")[-1][:80]

                results.append({
                    "title": title,
                    "url": full_url,
                    "slug": slug,
                    "tag": "乌尔西诺夫",
                    "category": "Daily",
                })

                if len(results) >= 3:
                    break

        if not results:
            print("ursynow_fetcher: no articles found in page HTML.")

        return results

    except Exception as e:
        # Never crash the engine — return empty list and log
        print(f"ursynow_fetcher failed: {e}")
        return []


def fetch_content(url):
    """Fetches article body text."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for selector in ["div.journal-content-article", "div#content", "article", "main"]:
            el = soup.select_one(selector)
            if el:
                return el.get_text(separator=" ", strip=True)

        return ""

    except Exception as e:
        print(f"ursynow_fetcher fetch_content failed for {url}: {e}")
        return ""
