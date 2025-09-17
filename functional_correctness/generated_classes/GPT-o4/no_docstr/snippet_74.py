class GetCh:
    def __init__(self):
        try:
            import msvcrt
            self.impl = lambda: msvcrt.getch().decode('utf-8', errors='ignore')
        except ImportError:
            import tty
            import termios
            def _unix_getch():
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch
            self.impl = _unix_getch

    def __call__(self):
        return self.impl()