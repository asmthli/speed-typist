import tkinter as tk


class Highscores(tk.Toplevel):
    def __init__(self, parent_window):
        super().__init__()
        parent_window.withdraw()
        self.focus_force()
        self.set_close_behaviour(parent_window)
        self.set_window_geometry(300, 300)

    def set_close_behaviour(self, parent_window):
        def close_and_restore():
            parent_window.deiconify()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", close_and_restore)

    def set_window_geometry(self, window_width, window_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width // 2 - window_width // 2
        y = screen_height // 2 - window_height // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")