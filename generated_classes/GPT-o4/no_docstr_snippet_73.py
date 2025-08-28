class TermStr:
    def __init__(self, *args):
        self._parts = []
        self._curattr = 0
        for arg in args:
            if isinstance(arg, int):
                self._curattr = arg
            else:
                s = str(arg)
                if s:
                    self._parts.append((s, self._curattr))

    def addstr(self, win, y=0, x=0):
        for s, attr in self._parts:
            try:
                win.addstr(y, x, s, attr)
            except TypeError:
                win.addstr(y, x, s)
            x += len(s)

    def __len__(self):
        return sum(len(s) for s, _ in self._parts)