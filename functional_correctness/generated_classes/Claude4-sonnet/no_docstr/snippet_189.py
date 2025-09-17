class TokenSetBuilder:
    def __init__(self):
        self.words = set()
        self.finished = False
        self.token_set = None

    def insert(self, word):
        if not self.finished:
            self.words.add(word.lower())

    def finish(self):
        self.finished = True
        self.token_set = frozenset(self.words)
        return self.token_set

    def minimize(self, down_to):
        if self.finished and len(self.words) > down_to:
            sorted_words = sorted(self.words, key=len, reverse=True)
            self.words = set(sorted_words[:down_to])
            self.token_set = frozenset(self.words)
        return self.token_set if self.finished else None