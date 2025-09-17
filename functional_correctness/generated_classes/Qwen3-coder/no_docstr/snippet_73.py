class TermStr:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            self.text = args[0]
        elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], int):
            self.text = args[0]
            self.attr = args[1]
        else:
            self.text = ""
            self.attr = 0

    def addstr(self, win, y=0, x=0):
        if hasattr(self, 'attr'):
            win.addstr(y, x, self.text, self.attr)
        else:
            win.addstr(y, x, self.text)

    def __len__(self):
        return len(self.text)