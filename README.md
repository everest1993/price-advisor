# Price-Advisor – Stima del prezzo di vendita con scraping + ML + OpenAI

Price-Advisor è uno script Python che combina:

- **scraping** (con Selenium)
- **filtraggio semantico e generazione di domande** (con OpenAI)
- **regressione lineare** (ML classico)

per stimare un **prezzo di vendita realistico** per un oggetto che vuoi vendere, partendo dagli annunci esistenti su un sito di annunci online.

---

## Disclaimer sullo scraping

> Lo scraping con Selenium è incluso **solo a scopo dimostrativo ed educativo**.  
> Fare scraping reale su siti in produzione può:
> - violare i **Termini di Servizio**,
> - violare le **policy** del sito,
> - in alcuni casi entrare in conflitto con la **normativa vigente**.
>
> Automatizzare l’accesso a siti web senza permesso **non è una buona pratica**: può causare problemi legali, etici e tecnici (ban IP, carico eccessivo sui server, ecc.).

---

## Funzionalità principali

- **Scraping automatico** degli annunci tramite **Selenium**
- Estrazione dei metadati essenziali (es. titolo, prezzo)
- **Filtro semantico** degli annunci tramite **API OpenAI**:
  - scarto degli annunci **non pertinenti**
  - assegnazione di un punteggio da **1 a 10** agli annunci pertinenti
- **Valutazione dell’oggetto dell’utente**:
  - OpenAI assegna un voto da **1 a 10** alla descrizione fornita
  - vengono generate **domande coerenti** per migliorare la descrizione
- **Modello di regressione lineare**:
  - allenato sui prezzi degli annunci ritenuti pertinenti
  - calcola un **prezzo di vendita consigliato**
  - la stima viene regolata in base al punteggio dell’oggetto

---

## Come funziona

1. **Input dell’utente**  
   L’utente descrive l’oggetto che vuole vendere, ad esempio:

   > “iPhone 13 128GB nero, buone condizioni, usato.”

2. **Scraping (Selenium)**  
   - Lo script apre il browser (es. Chrome) tramite Selenium.
   - Naviga verso il sito di annunci (URL definito nel codice o in una variabile d’ambiente).
   - Esegue una ricerca usando parole chiave correlate alla descrizione dell’utente.
   - Raccoglie una lista di annunci con:
     - titolo
     - prezzo

3. **Filtro e ranking con OpenAI**  
   - Gli annunci recuperati vengono inviati in batch a OpenAI.
   - Per ogni annuncio:
     - se è **non pertinente**, viene scartato;
     - se è pertinente, riceve un **punteggio da 1 a 10**.

4. **Valutazione dell’oggetto dell’utente**  
   - OpenAI valuta la descrizione fornita dall’utente e assegna un voto da **1 a 10**.
   - Se mancano informazioni importanti, lo script genera **domande mirate**, ad esempio:
     - “L’oggetto è ancora in garanzia?”
     - “Sono presenti graffi o difetti visibili?”
     - “Sono inclusi accessori originali?”

5. **Regressione lineare e stima del prezzo**  
   - A partire dagli annunci filtrati (con relativo prezzo) viene allenato un modello di **regressione lineare**.
   - Il modello calcola un **prezzo realistico di vendita**.

6. **Output**  
   Lo script restituisce il **prezzo consigliato** di vendita.

---

## Requisiti

- Python **3.9+**
- `pip` funzionante
- Account OpenAI con **API key valida**

Tutte le dipendenze Python (Selenium, client OpenAI, ecc.) sono elencate in `requirements.txt`.

---

## Installazione

### 1. Clona il repository

```bash
git clone https://github.com/everest1993/price-advisor
cd price-advisor
```

### 2. Crea e attiva l’ambiente virtuale

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
# .\.venv\Scripts\Activate.ps1

# Windows (cmd)
# .\.venv\Scripts\activate.bat
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

## Avvio

```bash
python price_advisor.py
```

---

## Licenza

Questo progetto è rilasciato sotto licenza [MIT](./LICENSE).

La licenza MIT consente di:

- usare il software per qualsiasi scopo,
- copiarlo, modificarlo, fonderlo in altri progetti,
- pubblicarlo, distribuirlo, sublicenziarlo e venderlo,

a condizione di **conservare il copyright** e il testo della licenza.

---

## Contribuire

Contributi, bugfix e idee sono benvenuti.

Linee guida di base:

1. **Forka** il repository su GitHub.
2. **Crea un branch** dedicato:

   ```bash
   git checkout -b feature/nome-feature
   ```

3. Assicurati che il codice:
   - non introduca regressioni evidenti,
   - mantenga il focus **didattico** e non incoraggi scraping aggressivo su siti reali.

4. Fai **commit chiari** (messaggi esplicativi).  
5. Fai **push** del branch e apri una **Pull Request** descrivendo:
   - cosa hai cambiato,
   - perché,
   - come testare la modifica.

---

## Nota legale ed etica (reminder finale)

- Rispetta sempre i **Termini di Servizio** dei siti che non controlli.
- Quando possibile, preferisci:
  - **API ufficiali** messe a disposizione dal sito,
  - **dataset open data**,
  - sandbox / siti di test.
- Limita il numero di richieste, evita scraping aggressivo, rispetta i server altrui.
- Considera questo progetto come un **esempio didattico** per:
  - usare Selenium in modo controllato,
  - integrare OpenAI per filtraggio e ranking semantico,
  - usare una regressione lineare per stimare prezzi in modo “data-driven”.