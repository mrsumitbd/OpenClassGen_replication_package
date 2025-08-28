class IniParser(object):
    def __init__(self, parser):
        self.parser = parser

    def get(self, section, key, default=None):
        try:
            return self.parser.get(section, key)
        except (KeyError, ValueError, AttributeError):
            return default