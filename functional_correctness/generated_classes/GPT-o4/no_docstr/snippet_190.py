class StringIndenter(object):
    def __init__(self):
        self._level = 0
        self._lines = []

    def dec(self, value, level=None):
        self._level = max(self._level - 1, 0)
        return self.render(value, level)

    def inc(self, value, level=None):
        self.render(value, level)
        self._level += 1
        return self

    def __call__(self, value, level=None):
        return self.render(value, level)

    def render(self, value, level=None):
        text = str(value)
        indent_str = self.indent(level)
        for line in text.split('\n'):
            self._lines.append(f"{indent_str}{line}")
        return self

    def indent(self, level=None):
        lvl = self._level if level is None else level
        return ' ' * (lvl * 4)

    def get(self):
        return '\n'.join(self._lines)