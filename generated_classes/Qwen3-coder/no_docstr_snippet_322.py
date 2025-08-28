class Widget(object):
    def __init__(self):
        self._handle_input = True
        self._read_only = False
        self._value = None
        self._subwidget = None

    def handle_key(self, key):
        # Handle a key press event
        # This is a basic implementation that can be overridden
        if not self.read_only:
            # Process the key input
            pass

    def get_subwidget(self):
        # Return the subwidget if it exists
        return self._subwidget

    @property
    def handle_input(self):
        # Return whether this widget handles input
        return self._handle_input

    @handle_input.setter
    def handle_input(self, value):
        # Set whether this widget handles input
        self._handle_input = bool(value)

    @property
    def read_only(self):
        # Return whether this widget is read-only
        return self._read_only

    @read_only.setter
    def read_only(self, value):
        # Set whether this widget is read-only
        self._read_only = bool(value)

    def get_value(self):
        # Return the current value of the widget
        return self._value

    def set_value(self, value):
        # Set the value of the widget
        if not self.read_only:
            self._value = value