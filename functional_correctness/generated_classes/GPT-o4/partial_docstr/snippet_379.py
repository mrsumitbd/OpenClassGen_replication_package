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
        decomposed = unicodedata.normalize('NFD', self.word)
        stripped = ''.join(ch for ch in decomposed if unicodedata.category(ch)[0] != 'M')
        return unicodedata.normalize('NFC', stripped)

    def ascii_encoding(self) -> str:
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
        base = self.remove_diacritics()
        mapping = {
            'Þ': 'th', 'þ': 'th',
            'Æ': 'ae', 'æ': 'ae',
            'Ƿ': 'w',  'ƿ': 'w',
            'Ð': 'd',  'ð': 'd'
        }
        return ''.join(mapping.get(ch, ch) for ch in base)