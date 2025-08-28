class Word:
    '''
    Transcription of Old English words
    '''

    def __init__(self, w: str):
        self.word = w

    def remove_diacritics(self) -> str:
        '''
        :return: str: the input string stripped of its diacritics

        Examples:

        >>> Word('ġelǣd').remove_diacritics()
        'gelæd'

        '''
        normalized = unicodedata.normalize('NFD', self.word)
        result = ''
        for char in normalized:
            if unicodedata.category(char) != 'Mn':
                result += char
        return result

    def ascii_encoding(self):
        '''
        :return: str: Returns the ASCII-encoded string

        Thorn (Þ, þ) and Ash(Æ, æ) are substituted by the digraphs
        'th' and 'ae' respectively. Wynn(Ƿ, ƿ) and Eth(Ð, ð) are replaced
        by 'w' and 'd'.

        Examples:

        >>> Word('ġelǣd').ascii_encoding()
        'gelaed'

        >>> Word('ƿeorðunga').ascii_encoding()
        'weordunga'

        '''
        # First remove diacritics
        text = self.remove_diacritics()
        
        # Replace Old English characters
        replacements = {
            'Þ': 'th',
            'þ': 'th',
            'Æ': 'ae',
            'æ': 'ae',
            'Ƿ': 'w',
            'ƿ': 'w',
            'Ð': 'd',
            'ð': 'd'
        }
        
        for old_char, new_char in replacements.items():
            text = text.replace(old_char, new_char)
        
        return text