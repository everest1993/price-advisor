from scraping.scraper import webScraper
from config import URL

scraper = webScraper(10)

# URL, nome prodotto, condizione (opzionale: nuovo, usato)
items = scraper.navigate_and_scrape(URL, "iphone 15", "usato")
if items:
    items.sort(key=lambda item: item["price"])

print(items)