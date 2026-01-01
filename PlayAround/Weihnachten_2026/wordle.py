import random

WORDS = [
    "apfel", "banjo", "clown", "dachs", "eimer",
    "fahne", "geist", "hotel", "insel", "joker",
    "koala", "lampe", "mango", "nacht", "orkan",
    "piano", "quarz", "radio", "sonne", "tiger",
    "uhren", "vogel", "wolke", "xenon", "yacht", "zebra"
]

MAX_TRIES = 6
WORD_LENGTH = 5


def get_feedback(guess, secret):
    feedback = ["⬜"] * WORD_LENGTH
    secret_list = list(secret)

    # 🟩 Richtige Position
    for i in range(WORD_LENGTH):
        if guess[i] == secret[i]:
            feedback[i] = "🟩"
            secret_list[i] = None

    # 🟨 Richtiger Buchstabe, falsche Position
    for i in range(WORD_LENGTH):
        if feedback[i] == "⬜" and guess[i] in secret_list:
            feedback[i] = "🟨"
            secret_list[secret_list.index(guess[i])] = None

    return "".join(feedback)


def print_intro():
    print("🎮 WORDLE (Python)")
    print("Errate das 5-Buchstaben-Wort!")
    print("🟩 richtig | 🟨 enthalten | ⬜ nicht enthalten")
    print("-" * 35)


def play_wordle():
    secret = random.choice(WORDS)
    tries = 0

    print_intro()

    while tries < MAX_TRIES:
        guess = input(f"Versuch {tries + 1}/{MAX_TRIES}: ").lower()

        if len(guess) != WORD_LENGTH or not guess.isalpha():
            print("❌ Bitte ein 5-Buchstaben-Wort eingeben.")
            continue

        tries += 1
        feedback = get_feedback(guess, secret)
        print(feedback)

        if guess == secret:
            print("🎉 Glückwunsch! Du hast das Wort erraten!")
            return

    print(f"💀 Verloren! Das Wort war: {secret}")


if __name__ == "__main__":
    play_wordle()
