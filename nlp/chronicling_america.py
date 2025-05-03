import requests
from time import sleep

TOP_US_STATES = [
     "California", "Texas", "Florida", "New York", "Pennsylvania",
    "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan"
]

def safe_get(url, params, retries=3, delay=2):
    for i in range(retries):
        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            print(f" Retry {i+1}/{retries} failed: {e}")
            sleep(delay * (i + 1))  # exponential backoff
    return None

def load_chronicling_articles_all_states(date1="1776", date2="1945", rows_per_state=20, delay_between_states=5):
    base_url = "https://chroniclingamerica.loc.gov/search/pages/results/"
    all_articles = []

    for state in TOP_US_STATES:
        print(f"🔍 Fetching articles for {state}...")

        params = {
            'format': 'json',
            'state': state,
            'date1': date1,
            'date2': date2,
            'rows': rows_per_state
        }

        res = safe_get(base_url, params)
        if not res:
            print(f" Skipping {state} after repeated failures.")
            continue

        for item in res.get('items', []):
            if not item.get("ocr_eng"):
                continue

            all_articles.append({
                "title": item.get("title", "Unknown"),
                "year": item.get("date", "Unknown")[:4],
                "region": state,
                "source": "Chronicling America",
                "text": item["ocr_eng"].strip()
            })

        sleep(delay_between_states)

    print(f"\n Collected {len(all_articles)} articles from all states.")
    return all_articles
