# medieval_sourcebook_loader.py

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://sourcebooks.fordham.edu"

def estimate_year(text):
    match = re.search(r'(\d{3,4})\s?(A\.?D\.?|C\.?E\.?)', text, re.IGNORECASE)
    return match.group(1) if match else "Medieval"

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "footer", "nav"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)

def load_medieval_articles(limit=30):
    collection_url = f"{BASE_URL}/sbook.asp"
    res = requests.get(collection_url)
    soup = BeautifulSoup(res.content, "html.parser")

    all_links = soup.select("ul li a[href^='/']")[:limit]  # grab first N articles
    results = []

    for link in all_links:
        href = link['href']
        title = link.text.strip()
        full_url = f"{BASE_URL}{href}"

        try:
            article_res = requests.get(full_url)
            article_text = clean_text(article_res.text)
            year = estimate_year(article_text)

            results.append({
                "title": title,
                "year": year,
                "region": "Europe/Global",  # can improve with URL filtering
                "source": "Internet Medieval Sourcebook",
                "text": article_text
            })
            print(f"✅ Scraped: {title}")

        except Exception as e:
            print(f"❌ Failed: {title} ({full_url}) — {e}")

    print(f"\n✅ Finished scraping {len(results)} medieval texts.")
    return results
