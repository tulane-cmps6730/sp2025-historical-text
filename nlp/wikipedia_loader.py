import wikipedia
import re

def estimate_date(text):
    match = re.search(r"(\d{3,4})\s?(BC|B\.C\.|BCE)", text, re.IGNORECASE)
    if match:
        return f"{match.group(1)} BC"
    match = re.search(r"(\d{1,3})\s?(AD|A\.D\.|CE)", text, re.IGNORECASE)
    if match:
        return f"{match.group(1)} AD"
    return "Unknown"

def load_ancient_articles(keyword="ancient", limit=200):
    results = []
    seen = set()

    search_pages = wikipedia.search(keyword, results=limit * 2)

    print(f"🔎 Searching Wikipedia for '{keyword}'... {len(search_pages)} results found.")
    for idx, title in enumerate(search_pages):
        if len(results) >= limit:
            break
        if title in seen:
            continue
        seen.add(title)

        print(f"⏳ [{idx+1}/{limit*2}] Fetching: {title}")
        try:
            page = wikipedia.page(title, auto_suggest=False, preload=False)
            text = page.content

            # Estimate date
            year = estimate_date(text)

            if "BC" in year or "AD" in year:
                results.append({
                    "title": page.title,
                    "year": year,
                    "region": "Global",
                    "source": "Wikipedia",
                    "text": text.strip()
                })
                print(f"✅ Added: {title} ({year})")
            else:
                print(f"⏩ Skipped (no date match): {title}")

        except Exception as e:
            print(f"❌ Error with '{title}': {e}")

    print(f"\n✅ Collected {len(results)} ancient articles from Wikipedia.")
    return results
