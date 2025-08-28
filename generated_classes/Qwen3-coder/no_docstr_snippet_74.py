class GetCh:
    def __init__(self):
        try:
            # Try to import Windows-specific modules
            import msvcrt
            self.impl = self._getch_windows
        except ImportError:
            # Fall back to Unix/Linux implementation
            try:
                import sys, tty, termios
                self.impl = self._getch_unix
            except ImportError:
                # If neither works, fall back to regular input
                self.impl = self._getch_fallback

    def __call__(self):
        return self.impl()

    def _getch_windows(self):
        import msvcrt
        return msvcrt.getch().decode('utf-8')

    def _getch_unix(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def _getch_fallback(self):
        return input()[0] if input() else ''