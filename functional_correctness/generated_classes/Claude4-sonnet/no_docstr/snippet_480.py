class User:
    def __init__(self, parent=None, id='', display_name=''):
        self.parent = parent
        self.id = id
        self.display_name = display_name

    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == 'ID':
            self.id = value
        elif name == 'DisplayName':
            self.display_name = value

    def to_xml(self, element_name='Owner'):
        xml = f'<{element_name}>'
        if self.id:
            xml += f'<ID>{self.id}</ID>'
        if self.display_name:
            xml += f'<DisplayName>{self.display_name}</DisplayName>'
        xml += f'</{element_name}>'
        return xml