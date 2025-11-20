import requests

# Die URL der lokalen Ollama-API
API_URL = "http://localhost:11434/api/generate"

# Das Modell, das du per "ollama pull mistral" geladen hast
MODEL = "mistral"

def ask_mistral(prompt: str) -> str:
    """
    Sendet eine Frage (prompt) an das lokale Mistral-Modell über die Ollama-API
    und gibt die Antwort als Text zurück.
    """

    payload = {
        "model": MODEL,   # welches Modell benutzt wird
        "prompt": prompt, # hier steht deine eigentliche Frage drin
        "stream": False   # gesamte Antwort auf einmal (kein Live-Streaming)
    }

    # Anfrage an die lokale API schicken
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()

    data = response.json()

    # Die eigentliche KI-Antwort zurückgeben
    return data.get("response", "")

if __name__ == "__main__":
    # 👉 HIER stellst du deine Frage!
    frage = "Erkläre mir den Unterschied zwischen einer Liste und einem Tuple in Python."

    antwort = ask_mistral(frage)

    print("Antwort von Mistral:")
    print(antwort)
