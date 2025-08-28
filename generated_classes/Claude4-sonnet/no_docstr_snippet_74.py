class GetCh:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)

    def __call__(self):
        try:
            tty.cbreak(self.fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
        return ch