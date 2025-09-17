class User:

    def __init__(self, parent=None, id='', display_name=''):
        self.parent = parent
        self.id = id
        self.display_name = display_name
        self._current = None

    def startElement(self, name, attrs, connection):
        if name == 'ID':
            self._current = 'id'
            return self
        if name == 'DisplayName':
            self._current = 'display_name'
            return self
        return None

    def endElement(self, name, value, connection):
        if name == 'ID':
            self.id = value
        elif name == 'DisplayName':
            self.display_name = value
        else:
            if self.parent is not None:
                setattr(self.parent, name, value)
        self._current = None

    def to_xml(self, element_name='Owner'):
        parts = [
            f'<{element_name}>',
            f'<ID>{escape(self.id)}</ID>',
            f'<DisplayName>{escape(self.display_name)}</DisplayName>',
            f'</{element_name}>'
        ]
        return ''.join(parts)