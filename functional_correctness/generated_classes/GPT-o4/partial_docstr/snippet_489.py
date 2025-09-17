class Renderable:
    '''A render-able (color or style) named object'''

    _BASE_COLOR_CODES = {
        "black": 30, "red": 31, "green": 32, "yellow": 33,
        "blue": 34, "magenta": 35, "cyan": 36, "white": 37
    }
    _STYLE_CODES = {
        "bold": 1, "underline": 4, "reversed": 7
    }

    def __init__(self, name):
        self.name = name
        parts = name.split("_")
        codes = []
        bright = "bright" in parts
        bg = "bg" in parts
        for p in parts:
            if p in self._STYLE_CODES:
                codes.append(self._STYLE_CODES[p])
            elif p in self._BASE_COLOR_CODES:
                base = self._BASE_COLOR_CODES[p]
                offset = (10 if bg else 0) + (60 if bright else 0)
                codes.append(base + offset)
        if codes:
            self._prefix = "\033[" + ";".join(str(c) for c in codes) + "m"
            self._suffix = "\033[0m"
        else:
            self._prefix = ""
            self._suffix = ""

    def __repr__(self):
        return f"<Renderable {self.name}>"

    def __call__(self, text, size=None):
        s = str(text)
        if size is not None:
            n = int(size)
            width = abs(n)
            if len(s) > width:
                s = s[:width]
            elif len(s) < width:
                if n > 0:
                    s = s.ljust(width)
                else:
                    s = s.rjust(width)
        return self.rendered(s)

    def rendered(self, text):
        return f"{self._prefix}{text}{self._suffix}"