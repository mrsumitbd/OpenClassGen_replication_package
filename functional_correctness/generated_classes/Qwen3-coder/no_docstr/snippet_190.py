class StringIndenter(object):
    def __init__(self):
        self._content = []
        self._current_level = 0
        self._indent_size = 4

    def dec(self, value, level=None):
        if level is None:
            level = self._current_level - 1
        self._current_level = max(0, level)
        self._content.append(self.indent(self._current_level) + str(value))
        return self

    def inc(self, value, level=None):
        if level is None:
            level = self._current_level + 1
        self._current_level = level
        self._content.append(self.indent(self._current_level) + str(value))
        return self

    def __call__(self, value, level=None):
        return self.render(value, level)

    def render(self, value, level=None):
        if level is None:
            level = self._current_level
        self._content.append(self.indent(level) + str(value))
        return self

    def indent(self, level=None):
        if level is None:
            level = self._current_level
        return ' ' * (level * self._indent_size)

    def get(self):
        return '\n'.join(self._content)