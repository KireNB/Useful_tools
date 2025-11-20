from openai import OpenAI

# ⚠️ Deinen API-Key direkt hier eintragen
API_KEY = "add_your_key"

# Client initialisieren
client = OpenAI(api_key=API_KEY)

def ask_chatgpt(prompt: str) -> str:
    """
    Sendet eine Anfrage an ChatGPT und gibt die Antwort zurück.
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user", "content": prompt}
        ]
    )

    # Antworttext extrahieren
    return response.choices[0].message.content


# Testaufruf
if __name__ == "__main__":
    frage = "Erkläre mir kurz, was eine API ist und nenne die wichtigsten Einsatzgebiete"
    antwort = ask_chatgpt(frage)
    print("Antwort von ChatGPT:")
    print(antwort)
