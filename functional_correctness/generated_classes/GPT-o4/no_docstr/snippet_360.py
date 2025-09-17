class IniParser(object):
    def __init__(self, parser):
        if isinstance(parser, configparser.ConfigParser):
            self._parser = parser
        else:
            self._parser = configparser.ConfigParser()
            self._parser.read(parser)

    def get(self, section, key, default=None):
        try:
            return self._parser.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default