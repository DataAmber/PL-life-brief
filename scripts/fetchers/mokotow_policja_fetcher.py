import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mokotow.policja.gov.pl"
LIST_URL = f"{BASE_URL}/r2/aktualnosci"


def fetch_list():
    """
    Returns up to 3 latest news items from the Mokotów/Ursynów/Wilanów
    police district (KRP II) news page.
    Covers: theft alerts, missing persons, safety warnings, scam notices.
    """
    response = requests.get(LIST_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    # The policja.gov.pl CMS renders articles as <div class="article-list-item">
    # with an <a> inside containing the title and href
    items = soup.select("div.article-list-item a, ul.article-list li a")

    # Fallback: scan all links whose href matches the article pattern
    if not items:
        items = [
            a for a in soup.find_all("a", href=True)
            if "/r2/aktualnosci/" in a.get("href", "")
            and a.get_text(strip=True)
        ]

    for a in items[:3]:
        href = a.get("href", "")
        title = a.get_text(strip=True)

        if not href or not title:
            continue

        full_url = BASE_URL + href if href.startswith("/") else href
        slug = "policja-" + href.rstrip("/").split("/")[-1][:80]

        results.append({
            "title": title,
            "url": full_url,
            "slug": slug,
            "tag": "治安安全",
            "category": "Daily",
        })

    return results


def fetch_content(url):
    """Fetches the full text of a specific police news article."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Try standard article containers used by policja.gov.pl CMS
    for selector in ["div#wtxt", "div.article-body", "article", "main"]:
        element = soup.select_one(selector)
        if element:
            return element.get_text(separator=" ", strip=True)

    return ""
  
