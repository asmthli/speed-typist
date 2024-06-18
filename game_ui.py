import tkinter
import tkinter as tk

from word_engine import WordEngine


class Game(tk.Toplevel):
    def __init__(self, parent_window):
        super().__init__()
        parent_window.withdraw()
        self.focus_force()
        self.set_close_behaviour(parent_window)
        self.set_window_geometry(900, 300)

        self.bg_colour = parent_window.bg_colour
        self.configure(bg=self.bg_colour)

        self.word_engine = WordEngine(num_sentences=80)

        self.create_static_widgets()
        self.current_letter_colour = "green"
        self.completed_letter_colour = "orange"
        self.main_textbox = self.create_main_textbox()
        self.wpm_counter = self.create_wpm_counter()

        # Testing
        self.set_character_as_current(1.0)

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
        textbox.insert(tk.END, self.word_engine.sentences)

        # Associate colours with tags so we can highlight letters later.
        textbox.tag_configure("current_letter", foreground=self.current_letter_colour)
        textbox.tag_configure("completed_letter", foreground=self.completed_letter_colour)

        textbox.pack()
        textbox.configure(state=tk.DISABLED)
        return textbox

    def set_character_as_current(self, char_index):
        self.main_textbox.tag_add("current_letter", char_index)

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
