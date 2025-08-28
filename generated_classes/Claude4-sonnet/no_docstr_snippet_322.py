class Widget(object):
    def __init__(self):
        self._handle_input = False
        self._read_only = False
        self._value = None
        self._subwidget = None

    def handle_key(self, key):
        return False

    def get_subwidget(self):
        return self._subwidget

    @property
    def handle_input(self):
        return self._handle_input

    @property
    def read_only(self):
        return self._read_only

    def get_value(self):
        return self._value