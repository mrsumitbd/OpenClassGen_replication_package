class Blink:
    def __init__(self):
        self._is_on = False

    def on(self):
        self._is_on = True
        return self

    def off(self):
        self._is_on = False
        return self

    def is_on(self):
        return self._is_on

    def is_off(self):
        return not self._is_on

    def toggle(self):
        self._is_on = not self._is_on
        return self