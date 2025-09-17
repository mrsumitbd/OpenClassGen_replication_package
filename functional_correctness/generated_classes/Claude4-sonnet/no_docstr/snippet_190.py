class StringIndenter(object):

    def __init__(self):
        self._level = 0
        self._indent_string = "    "

    def dec(self, value, level=None):
        if level is not None:
            self._level = max(0, level)
        else:
            self._level = max(0, self._level - 1)
        return self.render(value, self._level)

    def inc(self, value, level=None):
        if level is not None:
            self._level = level
        else:
            self._level += 1
        return self.render(value, self._level)

    def __call__(self, value, level=None):
        return self.render(value, level)

    def render(self, value, level=None):
        if level is None:
            level = self._level
        return self.indent(level) + str(value)

    def indent(self, level=None):
        if level is None:
            level = self._level
        return self._indent_string * level

    def get(self):
        return self._level