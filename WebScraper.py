import requests  # talks to websites (fetch HTML)
from bs4 import BeautifulSoup  # parses HTML (finds what you need)
import pandas as pd  # stores data into CSV/Excel

# Optional: progress bar library
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None  # if tqdm not installed, progress bar will not work

# ------------------------------
# CONFIGURATION
use_progress_bar = True  # True → show progress bar, False → normal output
base_url = "http://quotes.toscrape.com"  # change this to scrape a different website
max_pages = None  # set number of pages to scrape, None → scrape all pages
max_quotes = None  # set max number of quotes, None → no limit
# ------------------------------

# Lists to store all scraped data
quotes_list = []
authors_list = []
tags_list = []

page = 1
total_quotes = 0

print("Starting scraping... 🚀")

while True:
    # Stop if max pages reached
    if max_pages and page > max_pages:
        break

    url = f"{base_url}/page/{page}/"
    response = requests.get(url)  # fetch the page

    # Check if page fetched successfully
    if response.status_code != 200:
        print(f"Failed to fetch page {page}, stopping.")
        break

    soup = BeautifulSoup(response.text, "html.parser")  # parse HTML
    all_quotes = soup.find_all("div", class_="quote")  # find all quote containers

    # Stop loop if no quotes on page (end of website)
    if not all_quotes:
        print(f"No more quotes found on page {page}.")
        break

    # Decide whether to use progress bar or normal loop
    if use_progress_bar and tqdm:
        iterator = tqdm(all_quotes, desc=f"Scraping Page {page}", unit="quote")
    else:
        iterator = all_quotes

    for quote in iterator:
        # Stop if max quotes reached
        if max_quotes and total_quotes >= max_quotes:
            break

        # Quote text safely
        text_tag = quote.find(["span", "p"], class_="text")
        text = text_tag.get_text() if text_tag else "No text found"

        # Author safely
        author_tag = quote.find("small", class_="author")
        author = author_tag.get_text() if author_tag else "Unknown"

        # Tags safely
        tag_elements = quote.find_all("a", class_="tag")
        tags = [tag.get_text() for tag in tag_elements] if tag_elements else ["No tags"]

        # Append to lists
        quotes_list.append(text)
        authors_list.append(author)
        tags_list.append(", ".join(tags))  # comma-separated

        total_quotes += 1

    print(f"Page {page} scraped, {len(all_quotes)} quotes found.")
    
    # Stop if max quotes reached
    if max_quotes and total_quotes >= max_quotes:
        break

    page += 1  # move to next page

# Save all data
data = pd.DataFrame({
    "Quote": quotes_list,
    "Author": authors_list,
    "Tags": tags_list
})

# Save file names based on progress bar usage
if use_progress_bar:
    data.to_csv("quotes_final_progress.csv", index=False)
    data.to_excel("quotes_final_progress.xlsx", index=False)
else:
    data.to_csv("quotes_final.csv", index=False)
    data.to_excel("quotes_final.xlsx", index=False)

print(f"Scraping completed! Total quotes: {total_quotes} 📊")

# ------------------------------
# Tiny helper: preview first 10 quotes
print("\nPreview of first 10 quotes:")
print("-" * 50)
for i in range(min(10, len(data))):
    print(f"{i+1}. {data['Quote'][i]} — {data['Author'][i]} | Tags: {data['Tags'][i]}")
print("-" * 50)
