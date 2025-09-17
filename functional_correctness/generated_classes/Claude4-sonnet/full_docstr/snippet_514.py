class LineTokenizer:
    '''Tokenize text by line; designed for study of poetry.'''

    def __init__(self, language):
        '''Lower incoming language name and assemble variables.
        :type language: str
        :param language : Language for sentences tokenization.
        '''
        self.language = language.lower()

    def tokenize(self, untokenized_string: str, include_blanks=False):
        '''Tokenize lines by '\n'.

        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :param include_blanks: Boolean; If True, blanks will be preserved by "" in returned list of strings; Default is False.
        :rtype : list of strings
        '''
        lines = untokenized_string.split('\n')
        
        if include_blanks:
            return [line if line.strip() else "" for line in lines]
        else:
            return [line for line in lines if line.strip()]