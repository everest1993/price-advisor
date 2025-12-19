custom_tools = [
    {
        "type": "function",
        "name": "navigate_and_scrape",
        "description": "Usa questa funzione per trovare i prezzi del prodotto specificato, "
                       "scegliendo gli argomenti attraverso le parole chiave più appropriate per la ricerca, "
                       "secondo quanto richiesto dall'utente. Restituisce una lista di dizionari.",
        "parameters": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "string",
                    "description": "Parole chiave per effettuare la ricerca. Esempio 'iPhone 16'.",
                },
                "condition": {
                    "type": "string",
                    "description": "Parole chiave per specificare le condizioni degli oggetti da "
                                   "cercare. Le opzioni possibili sono 'nuovo' o 'usato'."
                                   "Se non specificato utilizza il valore None",
                }
            },
            "required": ["product", "condition"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]