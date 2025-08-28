class ColorTheme:
    '''Color theme.
    '''

    def __init__(self, textFormatClass):
        '''Constructor gets TextFormat class as parameter for avoid cross-import problems
        '''
        self.textFormatClass = textFormatClass
        self.formats = {}

    def getFormat(self, styleName):
        '''Returns TextFormat for particular style
        '''
        if styleName not in self.formats:
            self.formats[styleName] = self.textFormatClass()
        return self.formats[styleName]