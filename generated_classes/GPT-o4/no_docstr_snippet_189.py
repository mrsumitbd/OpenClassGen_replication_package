class TokenSetBuilder:
    class _Node:
        __slots__ = ("final", "transitions")
        def __init__(self):
            self.final = False
            self.transitions = {}

        def __hash__(self):
            items = tuple(sorted((ch, id(nd)) for ch, nd in self.transitions.items()))
            return hash((self.final, items))

        def __eq__(self, other):
            if self.final != other.final:
                return False
            if self.transitions.keys() != other.transitions.keys():
                return False
            for ch, nd in self.transitions.items():
                if other.transitions[ch] is not nd:
                    return False
            return True

    def __init__(self):
        self.root = self._Node()
        self.register = {}
        self.previous_word = ""
        self.frontier = [self.root]

    def insert(self, word):
        if word < self.previous_word:
            raise ValueError("Words must be inserted in non-decreasing lex order")
        # find common prefix length
        common = 0
        max_common = min(len(word), len(self.previous_word))
        while common < max_common and word[common] == self.previous_word[common]:
            common += 1
        # minimize states beyond common prefix
        self.minimize(common)
        # add suffix for the new word
        node = self.frontier[common]
        for ch in word[common:]:
            nxt = self._Node()
            node.transitions[ch] = nxt
            self.frontier.append(nxt)
            node = nxt
        node.final = True
        self.previous_word = word

    def minimize(self, down_to):
        # minimize all states deeper than down_to
        for i in range(len(self.frontier) - 1, down_to, -1):
            node = self.frontier.pop()
            parent = self.frontier[i - 1]
            ch = self.previous_word[i - 1]
            registered = self.register.get(node)
            if registered is not None:
                parent.transitions[ch] = registered
            else:
                self.register[node] = node

    def finish(self):
        self.minimize(0)
        return self.root