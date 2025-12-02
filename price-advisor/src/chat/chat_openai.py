from scraping.scraper import WebScraper
from chat.tools import custom_tools

from openai import OpenAI
from dotenv import load_dotenv

import os
import json


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
scraper = WebScraper(10)

chat = [
    {
        "role": "system",
        "content": (
            "Sei un'assistente digitale il cui compito è consigliare un prezzo di vendita per "
            "un determinato prodotto basandosi sui prezzi di oggetti simili venduti e ricavati "
            "attraverso il modulo scraper. Usa i tool che ti fornisco in modo adeguato, se necessario. "
            "Se chiedo cose fuori contesto o inappropriate rispondi 'Non sono autorizzato a rispondere. "
            "Le uniche informazioni che devi chiedere e che ti interessano sono il nome del prodotto e "
            "la condizione (nuovo, usato)'. "
            "Devi pormi domande per assegnare al prodotto che voglio vendere un voto da 1 a 10 "
            "basandoti su caratteristiche pertinenti al prodotto stesso (possono essere memoria, "
            "completezza, condizioni estetiche, parti non funzionanti per dispositivi elettronici o "
            "presenza di segni, pagine, sottolineature per libri). Scegli autonomamente le "
            "caratteristiche da indagare in base al prodotto da vendere. "
            "Quando ricevi dal tool 'navigate_and_scrape' un output con 'items' (lista di dizionari "
            "con 'header' e 'price'), devi:\n"
            "1) Scartare gli elementi non pertinenti alla vendita del prodotto principale (es. cover, "
            "accessori, cavi, pellicole, solo scatola, ecc.).\n"
            "2) Assegnare a ogni elemento rimanente un voto da 1 a 10 basandoti solo sul campo "
            "'header' (memoria, condizioni, completezza, rovinato, presenza di problemi.).\n"
            "3) Generare una lista di oggetti e un intero:\n"
            "   - 'items_scored': array di oggetti nel formato "
            "     {\"score\": <voto_intero_1_10>, \"price\": <prezzo_numero>} "
            "     (uno per ogni elemento filtrato, nello stesso ordine).\n"
            "   - 'rating': voto assegnato all'oggetto che vuole vendere l'utente (intero da 1 a 10).\n"
            "   Devi assicurarti che ogni elemento in 'items_scored' abbia sia 'score' che 'price'.\n"
            "4) Quando hai raccolto tutte le informazioni necessarie e hai già chiamato il tool, "
            "la tua RISPOSTA FINALE deve essere solo un JSON nel formato:\n"
            "{ \"items_scored\": [ {\"score\": v1, \"price\": p1}, {\"score\": v2, \"price\": p2}, ... ], "
            "\"rating\": voto }\n"
            "senza testo aggiuntivo.\n"
            "All'inizio di ogni nuova conversazione, nel PRIMO messaggio che invii devi sempre:\n"
            "- salutare l'utente,\n"
            "- spiegare in 2-4 frasi cosa puoi fare (scraping annunci simili, valutazione qualità, "
            "regressione sui prezzi per proporre un prezzo di vendita),\n"
            "- spiegare in breve come funzionerà il flusso (ti faccio qualche domanda sul prodotto, poi cerco annunci simili e calcolo un prezzo suggerito),\n"
            "- quindi chiedere qual è il prodotto che vuole vendere e in che condizione è.\n"
        )
    }
]


def use_tool(tool_call):
    """
    Funzione per utilizzare i custom tools definiti
    """
    print(f"[DEBUG] L'assistente ha chiamato il tool: {tool_call.name}")
    print(f"[DEBUG] Argomenti grezzi: {tool_call.arguments}")

    raw_args = tool_call.arguments or "{}"
    try:
        args = json.loads(raw_args)
    except json.JSONDecodeError:
        args = {}

    tool_result = None

    if tool_call.name == "navigate_and_scrape":
        try:
            items = scraper.navigate_and_scrape(**args)
            # items: lista di dict con almeno {"header": ..., "price": ...}
            tool_result = {"items": items}
        except Exception as e:
            tool_result = {"error": f"Errore nel tool navigate_and_scrape: {str(e)}"}
    else:
        tool_result = {"error": f"Tool {tool_call.name} non implementato nel backend."}

    if tool_result is None:
        tool_result = {"result": "Nessun dato disponibile"}

    chat.append(
        {
            "type": "function_call",
            "name": tool_call.name,
            "call_id": tool_call.call_id,
            "arguments": tool_call.arguments,
        }
    )
    chat.append(
        {
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": json.dumps(tool_result),
        }
    )


def ask_assistant(user_message: str):
    """
    Implementazione della chat
    """
    chat.append({"role": "user", "content": user_message})

    while True:
        ai_response = client.responses.create(
            model="gpt-5.1",
            input=chat,
            tools=custom_tools,
        )

        if not ai_response.output:
            answer = ai_response.output_text
            if answer:
                chat.append({"role": "assistant", "content": answer})
            return answer

        function_call = None
        for call in ai_response.output:
            if call.type == "function_call":
                function_call = call
                break

        if not function_call:
            answer = ai_response.output_text
            if answer:
                chat.append({"role": "assistant", "content": answer})
            return answer

        use_tool(function_call)