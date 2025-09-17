class TermStr:
    def __init__(self, *args):
        self.segments = []
        if len(args) == 1:
            if isinstance(args[0], str):
                self.segments.append((args[0], None))
            else:
                self.segments = list(args[0])
        elif len(args) == 2:
            self.segments.append((args[0], args[1]))
        else:
            i = 0
            while i < len(args):
                if i + 1 < len(args) and not isinstance(args[i + 1], str):
                    self.segments.append((args[i], args[i + 1]))
                    i += 2
                else:
                    self.segments.append((args[i], None))
                    i += 1

    def addstr(self, win, y=0, x=0):
        current_x = x
        for text, attr in self.segments:
            if attr is not None:
                win.addstr(y, current_x, text, attr)
            else:
                win.addstr(y, current_x, text)
            current_x += len(text)

    def __len__(self):
        return sum(len(text) for text, attr in self.segments)