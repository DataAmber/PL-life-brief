import requests
from bs4 import BeautifulSoup

def fetch_list():
    """Returns a list of the 3 latest alert metadata."""
    url = "https://www.gov.pl/web/gis/ostrzezenia"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    alert_elements = soup.find_all('div', class_='art-prev')
    
    results = []
    for element in alert_elements[:3]: 
        link_tag = element.find('a')
        if not link_tag: continue
        
        title = link_tag.find('div', class_='title').text.strip()
        full_url = "https://www.gov.pl" + link_tag['href']
        
        # Use the URL slug as a unique ID (e.g., 'public-warning-eggs')
        slug = link_tag['href'].split('/')[-1]
        
        results.append({
            "title": title,
            "url": full_url,
            "slug": slug,
            "tag": "Safety",
            "category": "Daily"
        })
    return results

def fetch_content(url):
    """Fetches the full text of a specific alert."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.find('article')
    return article.get_text(separator=' ', strip=True) if article else ""
