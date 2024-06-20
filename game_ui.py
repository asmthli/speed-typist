import tkinter as tk
from tkinter import ttk

from word_engine import WordEngine


class Game(tk.Toplevel):
    def __init__(self, parent_window):
        super().__init__()
        # Hide the parent window.
        parent_window.withdraw()

        self.set_close_behaviour(parent_window)
        self.set_window_geometry(900, 300)

        self.bg_colour = parent_window.bg_colour
        self.font = ("arial", 14, "bold italic")
        self.configure(bg=self.bg_colour)

        self.word_engine = WordEngine(num_sentences=80)

        self.focus_force()
        self.bind("<KeyPress>", func=self.handle_keypress)

        # Custom event for starting the game.
        self.bind("<<BeginGame>>", func=self.begin_game)

        # Create widgets
        self.title_label = self.create_title_label()
        self.countdown_timer = CountdownTimer(self, countdown_start=3)
        self.wpm_counter = WPMCounter(self)
        self.main_textbox = MainTextbox(self, self.word_engine)
        self.time_bar = TimeBar(self)

        self.set_widget_layouts()

    def create_title_label(self):
        title_label = tk.Label(master=self,
                               text="Speed Typer!",
                               bg=self.bg_colour,
                               font=self.font)
        return title_label

    def set_widget_layouts(self):
        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure(0, weight=1)

        self.title_label.grid(row=0, column=0)
        self.main_textbox.grid(row=1, column=0)
        self.wpm_counter.grid(row=2, column=0)
        self.time_bar.grid(row=3, column=0)
        self.countdown_timer.grid(row=4, column=0)

    def handle_keypress(self, event):
        char_pressed = event.char

        if char_pressed == self.word_engine.current_char:
            self.word_engine.advance_current_char()

            self.main_textbox.colour_characters()
            self.main_textbox.update_view()

            current_WPM = self.word_engine.words_per_min()
            self.wpm_counter.update_value(current_WPM)

    def begin_game(self, event):
        self.time_bar.start_timer()

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
        self.word_engine = word_engine
        self.insert(tk.END, self.word_engine.sentences)

        self.current_letter_colour = "green"
        self.completed_letter_colour = "orange"

        # Associate colours with tags, so we can highlight letters later.
        self.tag_configure("current_letter", foreground=self.current_letter_colour)
        self.tag_configure("completed_letter", foreground=self.completed_letter_colour)

        # Set first character as current.
        self.tag_add("current_letter", "1.0")

        # User control is specified by methods below.
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


class CountdownTimer(tk.Frame):
    def __init__(self, parent, countdown_start):
        super().__init__(master=parent)
        self.parent = parent

        self.label_counter = tk.IntVar(value=countdown_start)
        self.label = self.create_countdown_lbl()

        self.button = self.create_start_btn()
        self.button.pack()

    def countdown(self):
        if self.label_counter.get() != 0:
            self.label_counter.set(self.label_counter.get() - 1)
            self.after(1000, self.countdown)
        else:
            self.label.configure(textvariable=tk.StringVar(value="Go!"))
            self.event_generate("<<BeginGame>>")

    def switch_widgets(self):
        self.button.pack_forget()
        self.label.pack()

    def create_start_btn(self):
        def start_countdown():
            self.after(1000, self.countdown)
            self.switch_widgets()

        button = ttk.Button(master=self,
                            text="Start Countdown",
                            command=start_countdown)
        return button

    def create_countdown_lbl(self):
        return tk.Label(master=self,
                        bg=self.parent.bg_colour,
                        font=self.parent.font,
                        textvariable=self.label_counter)


class WPMCounter(tk.Label):
    def __init__(self, parent):
        self.counter_var = tk.StringVar(value="WPM: 0.00")

        super().__init__(master=parent,
                         textvariable=self.counter_var,
                         bg=parent.bg_colour,
                         font=("arial", 14, "bold"))

    def update_value(self, value):
        self.counter_var.set(f"WPM: {value:.2f}")


class TimeBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.time_progress = tk.IntVar(value=60)

        # Create widgets
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
