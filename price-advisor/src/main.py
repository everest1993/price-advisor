from scraping.scraper import webScraper
from data_processing.data_processer import DataProcesser
from config import URL

import numpy as np

scraper = webScraper(10)
processer = DataProcesser()

# URL, nome prodotto, condizione (opzionale: nuovo, usato)
items = scraper.navigate_and_scrape(URL, "charizard psa 10", "usato")

prices = None 

if items:
    items.sort(key=lambda item: item["price"])
    
    # conversione in np.ndarray
    prices = np.array([item["price"] for item in items])

# chatgpt deve decidere gli elementi della lista che sono coerenti con la ricerca: no cover, accessori ecc
# chatgpt deve dare un voto da 1 a 10 alla qualità dell'elemento basandosi sul titolo (o accesso descrizione)

# cleaning dei dati dagli outliers (quantili di default 25, 75)
prices_cleaned = processer.clean_data_from_outliers(prices)

# regressione lineare per restituire il voto consigliato

print(prices)
print(prices_cleaned)