import requests
import re
import time
from bs4 import BeautifulSoup

BASE_URL = "https://www.gutenberg.org"
CATEGORY_URL = "https://www.gutenberg.org/ebooks/search/?query=colonialism&submit_search=Go%21"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# === Region Detection ===
def detect_specific_regions(text):
    keywords = {
        "Spain": ["Spain", "Madrid", "Toledo", "Catalonia", "Castile", "Aragon"],
        "France": ["France", "Paris", "Brittany", "Normandy", "Gaul", "Bourbon"],
        "Italy": ["Italy", "Rome", "Florence", "Venice", "Naples", "Lombardy", "Papal"],
        "Germany": ["Germany", "Saxony", "Prussia", "Bavaria", "Holy Roman Empire"],
        "England": ["England", "London", "York", "Anglo-Saxon", "Tudor", "British"],
        "Ireland": ["Ireland", "Dublin", "Gaelic"],
        "Scotland": ["Scotland", "Edinburgh", "Highlands"],
        "Netherlands": ["Netherlands", "Flanders", "Dutch"],
        "Greece": ["Greece", "Athens", "Byzantine"],
        "Turkey": ["Turkey", "Ottoman", "Anatolia", "Constantinople"],
        "Middle East": ["Jerusalem", "Palestine", "Holy Land", "Syria", "Lebanon", "Israel"],
        #"North Africa": ["Carthage", "Alexandria", "Berber", "Moorish", "Maghreb", "Algeria", "Tunisia"],
        "Asia": ["Persia", "India", "China", "Silk Road", "Phillipines", "Japan", "Indochina"],
        "Americas": [
            "Mexico", "Peru", "Haiti", "Jamaica", "Caribbean", "Colony", "Plantation",
            "Virginia", "Massachusetts", "Maryland", "New York", "New Jersey", "New Hampshire", "New England",
            "North Carolina", "South Carolina", "Georgia", "Rhode Island", "Connecticut", "Delaware",
            "New Spain", "New France", "New Netherland", "New Granada", "New Mexico", "Louisiana", "Panama", "New Amsterdam"
        ],
        "Africa": ["Africa", "Cape Colony", "Zanzibar", "Sierra Leone", "Sudan", "Kongo", "Gambia", "Gold Coast", "Rhodesia", "West Africa", "Nigeria", "Volta", 
                   "Carthage", "Alexandria", "Berber", "Moorish", "Maghreb", "Algeria", "Tunisia"]
    }

    text_lower = text.lower()
    region_counts = {}

    for region, terms in keywords.items():
        count = sum(len(re.findall(rf"\b{re.escape(term.lower())}\b", text_lower)) for term in terms)
        if count > 0:
            region_counts[region] = count

    return max(region_counts, key=region_counts.get) if region_counts else "Unknown"

# === Year Extraction ===
def extract_year(author_str, title_str):
    year_match = re.search(r"(1[0-9]{3})", author_str or "")
    if year_match:
        year = int(year_match.group(1))
        if year > 1970:
            title_match = re.search(r"(1[0-9]{3})", title_str or "")
            return title_match.group(1) if title_match else str(year)
        return str(year)
    title_match = re.search(r"(1[0-9]{3})", title_str or "")
    return title_match.group(1) if title_match else "Unknown"

# === Helpers ===
def get_books_from_page(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.select(".booklink")

def get_txt_link(book_url):
    res = requests.get(book_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    link = soup.find("a", string=re.compile(r"Plain Text UTF-8", re.IGNORECASE))
    if link and link.get("href"):
        href = link["href"]
        if href.startswith("//"):
            return "https:" + href
        elif href.startswith("/"):
            return BASE_URL + href
        elif href.startswith("http"):
            return href
    return None

def get_book_authors(book_url):
    res = requests.get(book_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    authors = soup.find_all("a", itemprop="creator")
    return "; ".join([a.get_text(strip=True) for a in authors]) if authors else "Unknown"

def get_book_description(book_url):
    res = requests.get(book_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    desc = soup.find("div", itemprop="description")
    if desc:
        return desc.get_text(strip=True)
    content = soup.find("div", id="content")
    if content:
        first_p = content.find("p")
        if first_p:
            return first_p.get_text(strip=True)
    return ""

def get_book_language(book_url):
    res = requests.get(book_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    lang_cell = soup.find("th", string="Language")
    if lang_cell and lang_cell.find_next_sibling("td"):
        return lang_cell.find_next_sibling("td").get_text(strip=True)
    return "Unknown"

def extract_book_data(book_card):
    title = book_card.select_one(".title").text.strip()
    book_url = BASE_URL + book_card.select_one("a")["href"]
    return title, book_url

# === Main Loader ===
def load_gutenberg_colonial_texts(limit=200):
    results = []
    start = 1

    while len(results) < limit:
        page_url = f"{CATEGORY_URL}&start_index={start}"
        print(f"Scraping: {page_url}")
        books = get_books_from_page(page_url)
        if not books:
            break

        for book_card in books:
            if len(results) >= limit:
                break

            title, book_url = extract_book_data(book_card)
            print(f"Fetching: {title}")

            language = get_book_language(book_url)
            if language.lower() != "english":
                print(f"Skipped (not English): {title} [{language}]")
                continue

            author = get_book_authors(book_url)
            year = extract_year(author, title)
            description = get_book_description(book_url)
            txt_link = get_txt_link(book_url)
            if not txt_link:
                print(f"Skipped (no .txt): {title}")
                continue

            try:
                lines = requests.get(txt_link, headers=HEADERS).text.splitlines()
                text = "\n".join(lines[200:]).strip()
                if len(text) < 1000:
                    print(f"Skipped (too short): {title}")
                    continue
            except Exception as e:
                print(f"Error downloading text: {e}")
                continue

            combined_text = f"{title} {description} {text}"
            region = detect_specific_regions(combined_text)

            results.append({
                "title": title,
                "author": author,
                "year": year,
                "region": region,
                "source": "Project Gutenberg",
                "text": text[:50000]
            })

            time.sleep(1)

        start += 25

    print(f"Collected {len(results)} historical texts.")
    return results
