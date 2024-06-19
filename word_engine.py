import requests
import time


class WordEngine:
    def __init__(self, num_sentences):
        self.words_API_endpoint = "https://baconipsum.com/api/"
        self.words_API_params = {"type": "all-meat",
                                 "sentences": 40}
        self.sentences = self.fetch_words(num_sentences)

        self.current_char_index = 0
        self.current_char = self.sentences[self.current_char_index]

        self.word_boundaries = self.create_word_boundaries()
        self.next_word_boundary = self.word_boundaries.pop()

        self.words_completed = 0

        self.words_per_min = self.make_words_per_min_counter()

    def make_words_per_min_counter(self):
        seconds_elapsed = 0
        previous_time = time.time()

        def words_per_min():
            nonlocal seconds_elapsed, previous_time
            time_now = time.time()
            seconds_elapsed += time_now - previous_time
            previous_time = time_now

            if seconds_elapsed == 0:
                return 0
            else:
                minutes_elapsed = seconds_elapsed / 60
                return round(self.words_completed / minutes_elapsed, 2)

        return words_per_min

    def at_end_of_word(self) -> bool:
        if self.current_char_index == self.next_word_boundary:
            return True
        else:
            return False

    def create_word_boundaries(self):
        boundary_indices = []
        for idx, char in enumerate(self.sentences):
            if char == " ":
                boundary_indices.append(idx)
        return boundary_indices[::-1]

    def current_char_textbox_idx(self):
        return "1." + str(self.current_char_index)

    def advance_current_char(self):
        if self.current_char_index == self.next_word_boundary:
            self.next_word_boundary = self.word_boundaries.pop()

        self.current_char_index += 1
        self.current_char = self.sentences[self.current_char_index]

    def fetch_words(self, num_sentences):
        self.words_API_params["sentences"] = num_sentences
        response = requests.get(self.words_API_endpoint,
                                self.words_API_params)
        response.raise_for_status()
        json = response.json()
        return json[0]


if __name__ == "__main__":
    engine = WordEngine(70)
