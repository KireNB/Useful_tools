import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
import time

CARD_SIZE = 120
ROWS = 4
COLS = 4
FLIP_SPEED = 20


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Spiel")

        self.player_names = [
            simpledialog.askstring("Spieler", "Name von Spieler 1:"),
            simpledialog.askstring("Spieler", "Name von Spieler 2:")
        ]

        self.scores = [0, 0]
        self.current_player = 0
        self.flipped_cards = []
        self.lock = False

        self.load_images()
        self.create_board()
        self.create_ui()

    def load_images(self):
        self.back_image = Image.open("images/back.png").resize((CARD_SIZE, CARD_SIZE))
        self.back_photo = ImageTk.PhotoImage(self.back_image)

        image_paths = [f"images/img{i}.png" for i in range(1, 9)]
        images = [Image.open(p).resize((CARD_SIZE, CARD_SIZE)) for p in image_paths]
        self.card_images = images * 2
        random.shuffle(self.card_images)

    def create_ui(self):
        self.info = tk.Label(
            self.root,
            text=self.get_status_text(),
            font=("Arial", 14)
        )
        self.info.grid(row=ROWS, column=0, columnspan=COLS, pady=10)

    def get_status_text(self):
        return (
            f"{self.player_names[0]}: {self.scores[0]}    |    "
            f"{self.player_names[1]}: {self.scores[1]}\n"
            f"Am Zug: {self.player_names[self.current_player]}"
        )

    def create_board(self):
        self.buttons = []
        self.cards = []

        for i in range(ROWS * COLS):
            btn = tk.Label(self.root, image=self.back_photo, bd=2, relief="raised")
            btn.grid(row=i // COLS, column=i % COLS, padx=5, pady=5)
            btn.bind("<Button-1>", lambda e, idx=i: self.on_card_click(idx))
            self.buttons.append(btn)
            self.cards.append({
                "image": self.card_images[i],
                "matched": False
            })

    def on_card_click(self, index):
        if self.lock:
            return
        if self.cards[index]["matched"]:
            return
        if index in self.flipped_cards:
            return

        self.flip_card(index)

        self.flipped_cards.append(index)

        if len(self.flipped_cards) == 2:
            self.lock = True
            self.root.after(800, self.check_match)

    def flip_card(self, index):
        img = self.cards[index]["image"]
        self.animate_flip(self.buttons[index], img)

    def animate_flip(self, widget, front_image):
        for i in range(10):
            widget.config(width=CARD_SIZE - i * 10)
            widget.update()
            time.sleep(0.01)

        widget.config(image=ImageTk.PhotoImage(front_image))
        widget.image = ImageTk.PhotoImage(front_image)

        for i in range(10):
            widget.config(width=CARD_SIZE - (9 - i) * 10)
            widget.update()
            time.sleep(0.01)

    def check_match(self):
        i1, i2 = self.flipped_cards
        img1 = self.cards[i1]["image"]
        img2 = self.cards[i2]["image"]

        if img1 == img2:
            self.cards[i1]["matched"] = True
            self.cards[i2]["matched"] = True
            self.scores[self.current_player] += 1
        else:
            self.hide_card(i1)
            self.hide_card(i2)
            self.current_player = 1 - self.current_player

        self.flipped_cards = []
        self.lock = False
        self.info.config(text=self.get_status_text())

        if all(card["matched"] for card in self.cards):
            self.end_game()

    def hide_card(self, index):
        self.buttons[index].config(image=self.back_photo)

    def end_game(self):
        if self.scores[0] > self.scores[1]:
            winner = self.player_names[0]
        elif self.scores[1] > self.scores[0]:
            winner = self.player_names[1]
        else:
            winner = "Unentschieden"

        messagebox.showinfo("Spiel beendet", f"Gewinner: {winner}")
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    MemoryGame(root)
    root.mainloop()
