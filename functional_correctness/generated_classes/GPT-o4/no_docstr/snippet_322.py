class Widget(object):
    def __init__(self, value='', read_only=False, subwidget=None):
        self._value = value
        self._read_only = read_only
        self._subwidget = subwidget

    def handle_key(self, key):
        if self._read_only:
            return False
        if self._subwidget:
            return self._subwidget.handle_key(key)
        if key == '\b':
            self._value = self._value[:-1]
        else:
            self._value += key
        return True

    def get_subwidget(self):
        return self._subwidget

    @property
    def handle_input(self):
        return self.handle_key

    @property
    def read_only(self):
        return self._read_only

    def get_value(self):
        if self._subwidget:
            return self._subwidget.get_value()
        return self._value