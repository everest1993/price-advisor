from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

import re
import time

from config import REGEX_PRICE_1, REGEX_PRICE_2
from data_processing.data_processer import DataProcesser
from config import URL


# opzioni browser
options = Options()
options.add_argument("--incognito")
options.add_argument("start-maximized")
options.add_argument("--headless=new") # modalità senza interfaccia grafica

PAGINE = 3


class WebScraper:
    def __init__(self, wait_time: int) -> None:
        self.driver = webdriver.Chrome(options = options)
        self.wait = WebDriverWait(self.driver, wait_time)


    def navigate_and_scrape(self, product: str, condition: str = None) -> list:
        """
        Trova i prezzi degli ultimi articoli venduti su ebay del prodotto specificato
            - product = nome del prodotto
            - condition = "nuovo"/"usato" (opzionale)
        Restituisce la lista completa di articoli trovati nelle prime x pagine specificate.
        """
        try:
            self.driver.get(URL) # apre la pagina

            try:
                reject_cookies = self.wait.until(EC.element_to_be_clickable((By.ID, "gdpr-banner-decline")))
                reject_cookies.click() # rifiuta cookies
            
            except Exception as e:
                print(f"Si è verificato un errore durante il rifiuto dei cookies: {e}")

            advanced_search = self.driver.find_element(By.CLASS_NAME, "gh-search-button__advanced-link")
            advanced_search.click() # ricerca avanzata

            print(f"Ricerca nelle prime {PAGINE} pagine\nProdotto: {product} - condizioni: {condition}")

            # search bar
            search_bar = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="_nkw"]')))
            search_bar.click()
            search_bar.send_keys(product)

            sold_items = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/main/form/fieldset[2]/div[3]/span")
            sold_items.click() # filtro oggetti venduti
        
            match condition:
                case "nuovo":
                    nuovo = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/main/form/fieldset[5]/div[1]/span")
                    nuovo.click()
                case "usato":
                    usato = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/main/form/fieldset[5]/div[2]/span")
                    usato.click()
                case _: # non specificato
                    non_specificato = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/main/form/fieldset[5]/div[3]/span")
                    non_specificato.click()

            search_bar.send_keys(Keys.RETURN) # invio ricerca

            items_list = []

            # avanzamento pagina
            for pagina in range(1, PAGINE + 1):
                print(f"Scraping pagina {pagina}...")
                items_list.extend(self.scrape_items())

                if pagina == PAGINE:
                    break
                
                try:
                    next_page = self.driver.find_element(By.XPATH, '//a[@type="next"]')
                    next_page.click()
                    print(f"Navigazione alla pagina n. {pagina + 1}")

                except Exception as e:
                    print(f"Non sono state trovate {PAGINE} pagine.\nRicerca interrotta a pagina {pagina}.")
                    break # esce dal ciclo

            print(f"{len(items_list)} elementi trovati.")

            return items_list

        except Exception as e:
            print(f"Si è verificato un errore durante il fetch dei dati: {e}")

        finally:
            self.driver.quit()


    def scrape_items(self):
        """
        Trova i prezzi di tutti gli articoli presenti sulla pagina.
        Restituisce una lista di dizionari {"header", "price"}
        """
        results_table = self.wait.until(EC.presence_of_element_located((By.ID, "srp-river-results")))

        items = results_table.find_elements(By.CLASS_NAME, "su-card-container__content")

        new_list = []

        processer = DataProcesser() # convertitore testo - float

        for i in items:
            try:
                header = i.find_element(By.XPATH, './/span[@class="su-styled-text primary default"]').text
                price = i.find_element(By.XPATH, './/div[@class="s-card__attribute-row"]').text
                
                # controllo sulla forma del prezzo
                if not (re.match(REGEX_PRICE_1, price) or re.match(REGEX_PRICE_2, price)):
                    item = {
                        "header": header,
                        "price": processer.to_float(price)
                    }

                    new_list.append(item)
            except:
                print(f"Formato header non riconosciuto.")
        
        return new_list