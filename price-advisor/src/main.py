from chat.chat_openai import ask_assistant 
from model.linear_regression_model import LinearRegressionModel

import json


model = LinearRegressionModel()

while True:
    """
    Il filtraggio degli articoli non pertinenti viene eseguito dall'assistente ai.
    A ogni item ritornato dallo scraper e filtrato viene assegnato un voto da 1 a 10 per applicare
    una regressione lineare e fornire in output un valore adeguato al prezzo di vendita.
    """
    user_input = input("You: ")

    if user_input.lower().strip() in {"exit", "quit", "esci"}:
        break

    answer = ask_assistant(user_input)
    
    try:
        data = json.loads(answer)

        items = data["items_scored"]

        x = [float(item["score"]) for item in items]
        y = [float(item["price"]) for item in items]
        rating = float(data["rating"])
        
        # discesa del gradiente per calcolare i parametri del modello
        w, b = model.perform_gradient_descent(x, y, 0.0, 0.0, 0.001 , 1000) 

        selling_price = int(w * rating + b) # applicazione del modello al prodotto

        print(f"Assistant: puoi vendere l'articolo a {selling_price} EUR")
    except Exception as e:
        # risposta normale che non include i risultati
        print(f"Assistant: {answer}\n")