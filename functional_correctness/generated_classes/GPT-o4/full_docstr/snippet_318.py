class ColorTheme:
    '''Color theme.
    '''

    def __init__(self, textFormatClass):
        '''Constructor gets TextFormat class as parameter for avoid cross-import problems'''
        self._textFormatClass = textFormatClass
        self._formats = {}

    def getFormat(self, styleName):
        '''Returns TextFormat for particular style'''
        if styleName not in self._formats:
            self._formats[styleName] = self._textFormatClass(styleName)
        return self._formats[styleName]