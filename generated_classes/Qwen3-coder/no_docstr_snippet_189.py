class TokenSetBuilder:
    def __init__(self):
        self.words = set()
        self.finished = False
        self.minimized = False

    def insert(self, word):
        if self.finished:
            raise RuntimeError("Cannot insert after finish() has been called")
        self.words.add(word)

    def finish(self):
        if not self.finished:
            self.finished = True
        return self.words

    def minimize(self, down_to):
        if not self.finished:
            raise RuntimeError("finish() must be called before minimize()")
        if self.minimized:
            return self.words
            
        if len(self.words) <= down_to:
            self.minimized = True
            return self.words
            
        # Sort words by length and then lexicographically
        sorted_words = sorted(self.words, key=lambda x: (len(x), x))
        self.words = set(sorted_words[:down_to])
        self.minimized = True
        return self.words