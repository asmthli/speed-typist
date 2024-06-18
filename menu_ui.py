import tkinter as tk


def start_game():
    menu = Menu()
    menu.launch()


class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x300")
        self.title("Speed Typist")

    def launch(self):
        self.mainloop()

