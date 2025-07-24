

import tkinter as tk
import random

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("500x600")

        self.words = {
            "database": "A structured collection of organized data.",
            "computer": "An electronic device for processing data.",
            "engineering": "Application of science to design systems.",
            "machines": "Devices that perform tasks with parts.",
            "datascience": "Extracting insights from structured and unstructured data.",
            "nextgen": "Advanced or upcoming technologies."
        }

        self.word = random.choice(list(self.words.keys()))
        self.hint = self.words[self.word]
        self.guessed_letters = set()
        self.remaining_attempts = 6

        # UI Components
        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.canvas.pack(pady=20)

        self.hint_label = tk.Label(self.root, text=f"Hint: {self.hint}", font=("Helvetica", 12))
        self.hint_label.pack()

        self.word_label = tk.Label(self.root, text=self.get_display_word(), font=("Helvetica", 18))
        self.word_label.pack(pady=20)

        self.input_label = tk.Label(self.root, text="Guess a letter:", font=("Helvetica", 12))
        self.input_label.pack()

        self.entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.entry.pack(pady=10)

        self.guess_button = tk.Button(self.root, text="Guess", command=self.make_guess, font=("Helvetica", 12))
        self.guess_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=20)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, font=("Helvetica", 12))
        self.restart_button.pack(pady=10)
        self.restart_button.config(state=tk.DISABLED)

        self.draw_hangman()

    def get_display_word(self):
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    # def draw_hangman(self):
    #     self.canvas.delete("all")
    #     # Hangman base
    #     self.canvas.create_line(50, 250, 150, 250, width=2)
    #     self.canvas.create_line(100, 250, 100, 50, width=2)
    #     self.canvas.create_line(100, 50, 200, 50, width=2)
    #     self.canvas.create_line(200, 50, 200, 80, width=2)

    #     # Hangman parts based on attempts
    #     parts = [
    #         lambda: self.canvas.create_oval(180, 80, 220, 120, width=2),  # Head
    #         lambda: self.canvas.create_line(200, 120, 200, 180, width=2),  # Body
    #         lambda: self.canvas.create_line(200, 140, 170, 170, width=2),  # Left Arm
    #         lambda: self.canvas.create_line(200, 140, 230, 170, width=2),  # Right Arm
    #         lambda: self.canvas.create_line(200, 180, 170, 220, width=2),  # Left Leg
    #         lambda: self.canvas.create_line(200, 180, 230, 220, width=2),  # Right Leg
    #     ]
    #     for i in range(6 - self.remaining_attempts):
    #         parts[i]()


    def draw_hangman(self):
        self.canvas.delete("all")
        # Hangman base
        self.canvas.create_line(50, 250, 150, 250, width=2)
        self.canvas.create_line(100, 250, 100, 50, width=2)
        self.canvas.create_line(100, 50, 200, 50, width=2)
        self.canvas.create_line(200, 50, 200, 80, width=2)

        # Hangman parts based on attempts
        parts = [
            lambda: self.canvas.create_oval(180, 80, 220, 120, width=2),  # Head
            lambda: self.canvas.create_line(200, 120, 200, 180, width=2),  # Body
            lambda: self.canvas.create_line(200, 140, 170, 170, width=2),  # Left Arm
            lambda: self.canvas.create_line(200, 140, 230, 170, width=2),  # Right Arm
            lambda: self.canvas.create_line(200, 180, 170, 220, width=2),  # Left Leg
            lambda: self.canvas.create_line(200, 180, 230, 220, width=2),  # Right Leg
        ]
        for i in range(6 - self.remaining_attempts):
            parts[i]()

        # Draw tears and sad face if the game is lost
        if self.remaining_attempts == 0:
            # Draw sad face
            self.canvas.create_arc(190, 110, 210, 130, start=0, extent=180, style=tk.ARC, width=2)
            # Draw tears
            self.canvas.create_line(190, 120, 185, 140, fill="blue", width=2)
            self.canvas.create_line(210, 120, 215, 140, fill="blue", width=2)




        #  

    def make_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            self.result_label.config(text="Please enter a single valid letter.", fg="red")
            return

        if guess in self.guessed_letters:
            self.result_label.config(text="You already guessed that letter!", fg="red")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            self.result_label.config(text="Good guess!", fg="green")
            self.word_label.config(text=self.get_display_word())
            if set(self.word) <= self.guessed_letters:
                self.result_label.config(text="Congratulations! You guessed the word!", fg="green")
                self.end_game()
        else:
            self.result_label.config(text="Wrong guess!", fg="red")
            self.remaining_attempts -= 1
            self.draw_hangman()
            if self.remaining_attempts == 0:
                self.result_label.config(text=f"Game Over! The word was '{self.word}'.", fg="red")
                self.end_game()

    def end_game(self):
        self.entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)

    def restart_game(self):
        self.word = random.choice(list(self.words.keys()))
        self.hint = self.words[self.word]
        self.guessed_letters = set()
        self.remaining_attempts = 6

        self.word_label.config(text=self.get_display_word())
        self.result_label.config(text="")
        self.hint_label.config(text=f"Hint: {self.hint}")
        self.entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.draw_hangman()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()
