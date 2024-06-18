import tkinter as tk


class Game(tk.Toplevel):
    def __init__(self, parent_window):
        super().__init__()
        parent_window.withdraw()
        self.focus_force()
        self.set_close_behaviour(parent_window)
        self.set_window_geometry(900, 300)

        self.bg_colour = parent_window.bg_colour
        self.configure(bg=self.bg_colour)

        self.create_static_widgets()
        self.main_textbox = self.create_main_textbox()
        self.wpm_counter = self.create_wpm_counter()

    def create_static_widgets(self):
        title_lbl = tk.Label(master=self,
                             text="Speed Typer!",
                             bg=self.bg_colour,
                             font=("arial", 16, "bold italic"))
        title_lbl.pack()

    def create_main_textbox(self):
        textbox = tk.Text(master=self,
                          height=2,
                          wrap="none",
                          bg=self.bg_colour,
                          font=("arial", 24, "bold italic"))
        textbox.pack()
        return textbox

    def create_wpm_counter(self):
        wpm_counter = tk.StringVar(value="WPM: 0")
        tk.Label(master=self,
                 textvariable=wpm_counter,
                 bg=self.bg_colour,
                 font=("arial", 14, "bold")).pack()
        return wpm_counter

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
