import requests


class WordEngine:
    def __init__(self, num_sentences):
        self.words_API_endpoint = "https://baconipsum.com/api/"
        self.words_API_params = {"type": "all-meat",
                                 "sentences": 40}
        self.sentences = self.fetch_words(num_sentences)

        self.current_letter_idx = 0

    def fetch_words(self, num_sentences):
        self.words_API_params["sentences"] = num_sentences
        response = requests.get(self.words_API_endpoint,
                                self.words_API_params)
        response.raise_for_status()
        json = response.json()
        return json[0]


if __name__ == "__main__":
    engine = WordEngine(70)



