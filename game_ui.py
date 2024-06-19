import tkinter as tk
from tkinter import ttk

from word_engine import WordEngine


class Game(tk.Toplevel):
    def __init__(self, parent_window):
        super().__init__()
        parent_window.withdraw()
        self.focus_force()
        self.set_close_behaviour(parent_window)
        self.set_window_geometry(900, 300)

        self.word_engine = WordEngine(num_sentences=80)

        self.bg_colour = parent_window.bg_colour
        self.font = ("arial", 14, "bold italic")
        self.configure(bg=self.bg_colour)

        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure(0, weight=1)

        self.bind("<KeyPress>", func=self.handle_keypress)

        self.create_static_widgets()

        self.wpm_counter = WPMCounter(self)
        self.wpm_counter.grid(row=2, column=0)

        self.main_textbox = MainTextbox(self, self.word_engine)
        self.main_textbox.grid(row=1, column=0)

        self.time_bar = TimeBar(self)
        self.time_bar.grid(row=3, column=0)
        self.time_bar.start_timer()

    def handle_keypress(self, event):
        char_pressed = event.char

        if char_pressed == self.word_engine.current_char:
            if self.word_engine.at_end_of_word():
                self.word_engine.words_completed += 1

            self.word_engine.advance_current_char()

            self.main_textbox.colour_characters()
            self.main_textbox.update_view()

            self.wpm_counter.counter_var.set(value=self.word_engine.words_per_min())

    def create_static_widgets(self):
        title_lbl = tk.Label(master=self,
                             text="Speed Typer!",
                             bg=self.bg_colour,
                             font=("arial", 16, "bold italic"))
        title_lbl.grid(row=0, column=0)

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


class MainTextbox(tk.Text):
    def __init__(self, parent, word_engine):
        super().__init__(master=parent,
                         height=2,
                         wrap="none",
                         bg=parent.bg_colour,
                         font=("arial", 24, "bold italic"))

        self.current_letter_colour = "green"
        self.completed_letter_colour = "orange"

        self.word_engine = word_engine

        self.insert(tk.END, self.word_engine.sentences)

        # Associate colours with tags, so we can highlight letters later.
        self.tag_configure("current_letter", foreground=self.current_letter_colour)
        self.tag_configure("completed_letter", foreground=self.completed_letter_colour)

        # Set first character as current.
        self.tag_add("current_letter", "1.0")

        self.configure(state=tk.DISABLED)

        self.focus_force()

    def update_view(self):
        self.see(self.word_engine.current_char_textbox_idx(chars_ahead=20))

    def colour_characters(self):
        # Colour completed characters.
        # self.main_textbox.tag_remove(tagName="current_letter",
        #                              index1="current_letter.first")

        # Colour the current character.
        self.tag_add(tagName="current_letter",
                     index1=self.word_engine.current_char_textbox_idx())


class WPMCounter(tk.Label):
    def __init__(self, parent):
        self.counter_var = tk.StringVar(value="WPM: 0")

        super().__init__(master=parent,
                         textvariable=self.counter_var,
                         bg=parent.bg_colour,
                         font=("arial", 14, "bold"))


class TimeBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.time_progress = tk.IntVar(value=0)
        self.progress_bar = self.create_progress_bar()
        self.label = self.create_label()

        self.label.pack(side=tk.LEFT)
        self.progress_bar.pack(side=tk.LEFT)

    def create_progress_bar(self):
        progress_bar = ttk.Progressbar(master=self,
                                       variable=self.time_progress,
                                       maximum=60,
                                       length=300,)
        return progress_bar

    def create_label(self):
        label = tk.Label(master=self,
                         text="Time Remaining:",
                         bg=self.parent.bg_colour,
                         font=self.parent.font)
        return label

    def start_timer(self):
        def add_second():
            if self.time_progress != 0:
                self.time_progress.set(self.time_progress.get() - 1)
                self.after(1000, add_second)

        self.time_progress.set(60)
        self.after(1000, add_second)
