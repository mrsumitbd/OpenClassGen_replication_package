class LineTokenizer:
    '''Tokenize text by line; designed for study of poetry.'''

    def __init__(self, language):
        '''Lower incoming language name and assemble variables.
        :type language: str
        :param language : Language for sentences tokenization.
        '''
        self.language = language.lower()

    def tokenize(self, untokenized_string: str, include_blanks=False):
        '''Tokenize lines by '\\n'.

        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :param include_blanks: Boolean; If True, blanks will be preserved by "" in returned list of strings; Default is False.
        :rtype : list of strings
        '''
        text = untokenized_string.replace('\r\n', '\n').replace('\r', '\n')
        lines = text.split('\n')
        if not include_blanks:
            lines = [ln for ln in lines if ln.strip() != ""]
        return lines