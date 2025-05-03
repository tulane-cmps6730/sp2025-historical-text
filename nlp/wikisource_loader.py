import requests
from bs4 import BeautifulSoup
import re
import time

BASE_URL = "https://www.gutenberg.org"
CATEGORY_URL = "https://www.gutenberg.org/ebooks/bookshelf/447"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# === Region Detector ===
def detect_specific_regions(text):
    keywords = [
        "Spain", "France", "Italy", "Germany", "Portugal", "England", "Ireland",
        "Scotland", "Wales", "Netherlands", "Belgium", "Austria", "Switzerland",
        "Hungary", "Poland", "Russia", "Greece", "Turkey", "Jerusalem",
        "North Africa", "Asia", "Middle East", "Rome", "Byzantine"
    ]

    found = set()
    for country in keywords:
        if country.lower() in text.lower():
            found.add(country)

    return ", ".join(sorted(found)) if found else "Europe"

# === Extract Year from Author Metadata ===
def extract_year(author_str):
    match = re.search(r"(1[3-9][0-9]{2})", author_str or "")
    return match.group(1) if match else "Unknown"

# === Get Books from Paginated Index ===
def get_books_from_page(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.select(".booklink")

# === Extract Book Info from Card ===
def extract_book_data(book_card):
    title = book_card.select_one(".title").text.strip()
    author_elem = book_card.select_one(".subtitle")
    author = author_elem.text.strip() if author_elem else "Unknown"
    year = extract_year(author)
    book_url = BASE_URL + book_card.select_one("a")["href"]
    return title, author, year, book_url

# === Get Book Description (for region detection) ===
def get_book_description(book_url):
    res = requests.get(book_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    desc_elem = soup.find("div", {"id": "about"})
    if desc_elem:
        return desc_elem.get_text(separator=" ", strip=True)
    return ""

# === Get .txt Download Link ===
def get_txt_link(book_url):
    res = requests.get(book_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("a[href$='.txt']")
    for link in links:
        href = link["href"]
        if "utf-8" in href or href.endswith(".txt"):
            return BASE_URL + href
    return None

# === Main Loader Function ===
def load_gutenberg_european_history(limit=10):
    results = []
    start = 1
    while len(results) < limit:
        paginated_url = f"{CATEGORY_URL}?start_index={start}"
        print(f"\n📚 Scraping: {paginated_url}")
        books = get_books_from_page(paginated_url)
        if not books:
            break

        for book_card in books:
            if len(results) >= limit:
                break

            title, author, year, book_url = extract_book_data(book_card)
            print(f"🔍 {title} ({year})")

            description = get_book_description(book_url)
            region = detect_specific_regions(description)

            txt_link = get_txt_link(book_url)
            if not txt_link:
                print(f"⏭ Skipped (no .txt): {title}")
                continue

            try:
                text_res = requests.get(txt_link, headers=HEADERS)
                text = text_res.text.strip()
                if len(text) < 1000:
                    print(f"⚠️ Skipped (text too short): {title}")
                    continue
            except Exception as e:
                print(f"⚠️ Error downloading text: {e}")
                continue

            results.append({
                "title": title,
                "author": author,
                "year": year,
                "region": region,
                "source": "Project Gutenberg",
                "text": text[:50000]  # limit for now
            })

            time.sleep(1)

        start += 25

    print(f"\n✅ Collected {len(results)} historical texts.")
    return results
