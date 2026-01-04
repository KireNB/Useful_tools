import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import random
import pygame
import os

CARD_SIZE = 120
ROWS = 4
COLS = 4

# Sounds
FLIP_SOUND = "sounds/flip.mp3"
MATCH_SOUND = "sounds/match.mp3"
FAIL_SOUND = "sounds/fail.mp3"

pygame.mixer.init(frequency=44100, size=-16, channels=2)

def play_sound(path):
    if os.path.exists(path):
        pygame.mixer.Sound(path).play()

def round_corners(im, rad):
    im = im.convert("RGBA")
    circle = Image.new("L", (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new("L", im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Spiel")
        self.root.configure(bg="#2E3440")
        self.show_start_menu()

    # ---------- STARTMENÜ ----------
    def show_start_menu(self):
        self.menu = tk.Frame(self.root, bg="#3B4252", padx=30, pady=30)
        self.menu.pack(expand=True)

        tk.Label(
            self.menu,
            text="Memory Spiel",
            font=("Arial", 24, "bold"),
            bg="#3B4252",
            fg="white"
        ).pack(pady=10)

        self.p1_entry = tk.Entry(self.menu, font=("Arial", 14))
        self.p1_entry.insert(0, "Spieler 1")
        self.p1_entry.pack(pady=5)

        self.p2_entry = tk.Entry(self.menu, font=("Arial", 14))
        self.p2_entry.insert(0, "Spieler 2")
        self.p2_entry.pack(pady=5)

        tk.Button(
            self.menu,
            text="Spiel starten",
            font=("Arial", 14),
            bg="#A3BE8C",
            command=self.start_game
        ).pack(pady=20)

    def start_game(self):
        self.players = [self.p1_entry.get(), self.p2_entry.get()]
        if not self.players[0] or not self.players[1]:
            messagebox.showerror("Fehler", "Bitte beide Namen eingeben")
            return

        self.menu.destroy()

        self.scores = [0, 0]
        self.current_player = 0
        self.flipped = []
        self.lock = False

        self.load_images()
        self.create_ui()

    # ---------- SPIEL ----------
    def load_images(self):
        back = Image.open("images/back.png").resize((CARD_SIZE, CARD_SIZE))
        self.back_photo = ImageTk.PhotoImage(round_corners(back, 20))

        self.front_photos = []
        for i in range(1, 9):
            img = Image.open(f"images/img{i}.png").resize((CARD_SIZE, CARD_SIZE))
            self.front_photos.append(
                ImageTk.PhotoImage(round_corners(img, 20))
            )

        self.cards = []
        for idx, photo in enumerate(self.front_photos):
            self.cards.append({"id": idx, "photo": photo, "matched": False})
            self.cards.append({"id": idx, "photo": photo, "matched": False})

        random.shuffle(self.cards)

    def create_ui(self):
        self.score_label = tk.Label(
            self.root,
            text=self.get_status_text(),
            font=("Arial", 14),
            bg="#2E3440",
            fg="white"
        )
        self.score_label.pack(pady=10)

        self.board = tk.Frame(self.root, bg="#2E3440")
        self.board.pack()

        self.buttons = []
        for i in range(ROWS * COLS):
            lbl = tk.Label(self.board, image=self.back_photo, bg="#2E3440", bd=0)
            lbl.grid(row=i // COLS, column=i % COLS, padx=8, pady=8)
            lbl.bind("<Button-1>", lambda e, idx=i: self.on_click(idx))
            self.buttons.append(lbl)

    def get_status_text(self):
        return (
            f"{self.players[0]}: {self.scores[0]}   |   "
            f"{self.players[1]}: {self.scores[1]}   "
            f"(Am Zug: {self.players[self.current_player]})"
        )

    def on_click(self, index):
        if self.lock or self.cards[index]["matched"] or index in self.flipped:
            return

        # 1. Karte
        if len(self.flipped) == 0:
            play_sound(FLIP_SOUND)

        self.buttons[index].config(image=self.cards[index]["photo"])
        self.flipped.append(index)

        # 2. Karte → SOFORT Sound abspielen
        if len(self.flipped) == 2:
            i1, i2 = self.flipped
            if self.cards[i1]["id"] == self.cards[i2]["id"]:
                play_sound(MATCH_SOUND)
            else:
                play_sound(FAIL_SOUND)

            self.lock = True
            self.root.after(2000, self.check_match)

    def check_match(self):
        i1, i2 = self.flipped
        c1 = self.cards[i1]
        c2 = self.cards[i2]

        if c1["id"] == c2["id"]:
            c1["matched"] = True
            c2["matched"] = True
            self.scores[self.current_player] += 1
        else:
            self.buttons[i1].config(image=self.back_photo)
            self.buttons[i2].config(image=self.back_photo)
            self.current_player = 1 - self.current_player

        self.flipped.clear()
        self.lock = False
        self.score_label.config(text=self.get_status_text())

        if all(card["matched"] for card in self.cards):
            self.end_game()

    # ---------- ENDE ----------
    def end_game(self):
        if self.scores[0] > self.scores[1]:
            msg = f"Gewonnen hat: {self.players[0]}\nPunkte: {self.scores[0]}"
        elif self.scores[1] > self.scores[0]:
            msg = f"Gewonnen hat: {self.players[1]}\nPunkte: {self.scores[1]}"
        else:
            msg = (
                "Unentschieden!\n\n"
                f"{self.players[0]}: {self.scores[0]} Punkte\n"
                f"{self.players[1]}: {self.scores[1]} Punkte"
            )

        messagebox.showinfo("Spiel beendet", msg)
        self.root.quit()

# ---------- START ----------
if __name__ == "__main__":
    root = tk.Tk()
    MemoryGame(root)
    root.mainloop()


# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk, ImageDraw
# import random
# import pygame
# import os
# import sys

# CARD_SIZE = 120
# ROWS = 4
# COLS = 4

# # Sounds
# FLIP_SOUND = "sounds/flip.mp3"
# MATCH_SOUND = "sounds/match.mp3"
# FAIL_SOUND = "sounds/fail.mp3"

# pygame.mixer.init()

# def play_sound(path):
#     if os.path.exists(path):
#         pygame.mixer.Sound(path).play()

# # Abgerundete Ecken
# def round_corners(im, rad):
#     im = im.convert("RGBA")
#     circle = Image.new("L", (rad * 2, rad * 2), 0)
#     draw = ImageDraw.Draw(circle)
#     draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)

#     alpha = Image.new("L", im.size, 255)
#     w, h = im.size
#     alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
#     alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
#     alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
#     alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
#     im.putalpha(alpha)
#     return im

# class MemoryGame:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Memory Spiel")
#         self.root.configure(bg="#2E3440")

#         self.flipped = []
#         self.lock = False
#         self.scores = [0, 0]
#         self.current_player = 0

#         self.load_images()
#         self.create_ui()

#     def load_images(self):
#         # Rückseite
#         back = Image.open("images/back.png").resize((CARD_SIZE, CARD_SIZE))
#         back = round_corners(back, 20)
#         self.back_photo = ImageTk.PhotoImage(back)

#         # Vorderseiten
#         self.front_photos = []
#         for i in range(1, 9):
#             img = Image.open(f"images/img{i}.png").resize((CARD_SIZE, CARD_SIZE))
#             img = round_corners(img, 20)
#             self.front_photos.append(ImageTk.PhotoImage(img))

#         # Kartenstapel (ID + Bild)
#         self.cards = []
#         for idx, photo in enumerate(self.front_photos):
#             self.cards.append({"id": idx, "photo": photo, "matched": False})
#             self.cards.append({"id": idx, "photo": photo, "matched": False})

#         random.shuffle(self.cards)

#     def create_ui(self):
#         self.score_label = tk.Label(
#             self.root,
#             text=self.get_status_text(),
#             font=("Arial", 14),
#             bg="#2E3440",
#             fg="white"
#         )
#         self.score_label.pack(pady=10)

#         self.board = tk.Frame(self.root, bg="#2E3440")
#         self.board.pack()

#         self.buttons = []

#         for i in range(ROWS * COLS):
#             lbl = tk.Label(
#                 self.board,
#                 image=self.back_photo,
#                 bg="#2E3440",
#                 bd=0
#             )
#             lbl.grid(row=i // COLS, column=i % COLS, padx=8, pady=8)
#             lbl.bind("<Button-1>", lambda e, idx=i: self.on_click(idx))
#             self.buttons.append(lbl)

#     def get_status_text(self):
#         return f"Spieler 1: {self.scores[0]} | Spieler 2: {self.scores[1]}  (Am Zug: Spieler {self.current_player + 1})"

#     def on_click(self, index):
#         if self.lock or self.cards[index]["matched"] or index in self.flipped:
#             return

#         play_sound(FLIP_SOUND)
#         self.buttons[index].config(image=self.cards[index]["photo"])
#         self.flipped.append(index)

#         if len(self.flipped) == 2:
#             self.lock = True
#             self.root.after(800, self.check_match)

#     def check_match(self):
#         i1, i2 = self.flipped
#         c1 = self.cards[i1]
#         c2 = self.cards[i2]

#         if c1["id"] == c2["id"]:
#             c1["matched"] = True
#             c2["matched"] = True
#             self.scores[self.current_player] += 1
#             play_sound(MATCH_SOUND)
#         else:
#             self.buttons[i1].config(image=self.back_photo)
#             self.buttons[i2].config(image=self.back_photo)
#             play_sound(FAIL_SOUND)
#             self.current_player = 1 - self.current_player

#         self.flipped.clear()
#         self.lock = False
#         self.score_label.config(text=self.get_status_text())

#         if all(card["matched"] for card in self.cards):
#             self.end_game()

#     def end_game(self):
#         if self.scores[0] > self.scores[1]:
#             winner = "Spieler 1"
#         elif self.scores[1] > self.scores[0]:
#             winner = "Spieler 2"
#         else:
#             winner = "Unentschieden"

#         messagebox.showinfo("Spiel beendet", f"Ergebnis: {winner}")
#         self.root.quit()

# if __name__ == "__main__":
#     root = tk.Tk()
#     MemoryGame(root)
#     root.mainloop()
