import requests
from bs4 import BeautifulSoup
import re
import time

BASE_URL = "https://www.gutenberg.org"
CATEGORY_URL = "https://www.gutenberg.org/ebooks/bookshelf/447"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def detect_specific_regions(text):
    keywords = {
        "Spain": ["Spain", "Madrid", "Toledo", "Catalonia", "Castile", "Aragon"],
        "France": ["France", "Paris", "Brittany", "Normandy", "Gaul", "Bourbon"],
        "Italy": ["Italy", "Rome", "Florence", "Venice", "Naples", "Lombardy", "Papal"],
        "Germany": ["Germany", "Saxony", "Prussia", "Bavaria", "Holy Roman Empire"],
        "England": ["England", "London", "York", "Anglo-Saxon", "Tudor"],
        "Ireland": ["Ireland", "Dublin", "Gaelic"],
        "Scotland": ["Scotland", "Edinburgh", "Highlands"],
        "Netherlands": ["Netherlands", "Flanders", "Dutch"],
        "Greece": ["Greece", "Athens", "Byzantine"],
        "Turkey": ["Turkey", "Ottoman", "Anatolia", "Constantinople"],
        "Middle East": ["Jerusalem", "Palestine", "Holy Land"],
        "North Africa": ["Carthage", "Alexandria", "Berber", "Moorish", "Maghreb"],
        "Asia": ["Persia", "India", "China", "Silk Road"]
    }

    text_lower = str(text).lower()
    regions_found = set()

    for region, terms in keywords.items():
        for term in terms:
            if re.search(rf"\b{re.escape(term.lower())}\b", text_lower):
                regions_found.add(region)

    return ", ".join(sorted(regions_found)) if regions_found else "Europe"

def extract_year_range(author_str, title_str):
    first_author = author_str.split(";")[0] if author_str else ""
    clean = re.sub(r"[^\d\–\- ]", "", first_author)

    match = re.search(r"(1[0-9]{3})[\–\-](1[0-9]{3})", clean)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        if start > 1600 or end > 1600:
            return "1300–1700"
        return f"{start}–{end}"

    years = [int(y) for y in re.findall(r"(1[0-9]{3})", clean) if int(y) <= 1600]
    if years:
        return str(max(years))

    match = re.search(r"(1[0-9]{3})[\–\-](1[0-9]{3})", title_str or "")
    if match:
        return f"{match.group(1)}–{match.group(2)}"
    match = re.search(r"(1[0-9]{3})", title_str or "")
    if match:
        return match.group(1)

    return "Unknown"

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

def get_books_from_page(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.select(".booklink")

def extract_book_data(book_card):
    title = book_card.select_one(".title").text.strip()
    book_url = BASE_URL + book_card.select_one("a")["href"]
    return title, book_url

def load_gutenberg_european_history(limit=50):
    results = []
    start = 1

    while len(results) < limit:
        page_url = f"{CATEGORY_URL}?start_index={start}"
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
            year = extract_year_range(author, title)
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

            region = detect_specific_regions(description)
            if region == "Europe":
                region = detect_specific_regions(text)

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
