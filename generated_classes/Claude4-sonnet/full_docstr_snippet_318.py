class ColorTheme:
    '''Color theme.
    '''

    def __init__(self, textFormatClass):
        '''Constructor gets TextFormat class as parameter for avoid cross-import problems
        '''
        self._textFormatClass = textFormatClass
        self._formats = {}
        self._initializeDefaultFormats()
    
    def _initializeDefaultFormats(self):
        '''Initialize default text formats for common styles
        '''
        self._formats = {
            'default': self._textFormatClass(),
            'keyword': self._textFormatClass(color='blue', bold=True),
            'string': self._textFormatClass(color='green'),
            'comment': self._textFormatClass(color='gray', italic=True),
            'number': self._textFormatClass(color='red'),
            'operator': self._textFormatClass(color='black', bold=True),
            'function': self._textFormatClass(color='purple'),
            'class': self._textFormatClass(color='darkblue', bold=True),
            'error': self._textFormatClass(color='red', bold=True),
            'warning': self._textFormatClass(color='orange')
        }

    def getFormat(self, styleName):
        '''Returns TextFormat for particular style
        '''
        return self._formats.get(styleName, self._formats['default'])