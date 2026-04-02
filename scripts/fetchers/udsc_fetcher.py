import requests
from bs4 import BeautifulSoup

def fetch_list():
    """Returns a list of the 3 latest news items from the Office for Foreigners (UDSC)."""
    url = "https://www.gov.pl/web/udsc-en/news-OFF"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    alert_elements = soup.find_all('div', class_='art-prev')
    results = []
    for element in alert_elements[:3]:
        link_tag = element.find('a')
        if not link_tag:
            continue

        title_tag = link_tag.find('div', class_='title')
        title = title_tag.text.strip() if title_tag else ""
        href = link_tag.get('href')
        if not href:
            continue

        full_url = "https://www.gov.pl" + href
        slug = "udsc-" + href.split('/')[-1]  # prefix to avoid slug collision with GIS
        results.append({
            "title": title,
            "url": full_url,
            "slug": slug,
            "tag": "Immigration",
            "category": "Daily"
        })
    return results

def fetch_content(url):
    """Fetches the full text of a specific UDSC news article."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article')
    return article.get_text(separator=' ', strip=True) if article else ""
