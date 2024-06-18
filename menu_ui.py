import tkinter as tk
from tkinter import font


def start_game():
    menu = Menu()
    menu.launch()


class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x300")
        self.title("Speed Typist")

        self.create_title()
        self.create_buttons()

        self.grid_rowconfigure(index=(0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(index=(0,), weight=1)

    def launch(self):
        self.mainloop()

    def create_title(self):
        title = tk.Label(master=self, text="Speed Typist!", font=("arial", 20, "bold underline"))
        title.grid(row=0, column=0)
        return title

    def create_buttons(self):
        play_game_btn = self.create_play_game_btn()
        highscores_btn = self.create_highscore_btn()
        quit_btn = self.create_quit_btn()

        play_game_btn.grid(row=1, column=0)
        highscores_btn.grid(row=2, column=0)
        quit_btn.grid(row=3, column=0)

    def create_play_game_btn(self):
        def play_game():
            print("Play game")

        return tk.Button(master=self, text="Play", command=play_game)

    def create_highscore_btn(self):
        def show_highscores():
            print("Highscores")

        return tk.Button(master=self, text="Highscores", command=show_highscores)

    def create_quit_btn(self):
        def quit_game():
            print("Quit game")

        return tk.Button(master=self, text="Quit", command=quit_game)

