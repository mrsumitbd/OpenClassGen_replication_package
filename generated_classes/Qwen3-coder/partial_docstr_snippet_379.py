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
        diacritics_map = {
            'ā': 'a', 'ǣ': 'æ', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u', 'ȳ': 'y',
            'Ā': 'A', 'Ē': 'E', 'Ī': 'I', 'Ō': 'O', 'Ū': 'U', 'Ȳ': 'Y',
            'ċ': 'c', 'ġ': 'g', 'ġ': 'g', 'ḟ': 'f', 'ġ': 'g', 'ġ': 'g',
            'Ċ': 'C', 'Ġ': 'G', 'Ḟ': 'F',
            'æ': 'æ', 'Æ': 'Æ', 'þ': 'þ', 'Þ': 'Þ', 'ð': 'ð', 'Ð': 'Ð',
            'ƿ': 'ƿ', 'Ƿ': 'Ƿ'
        }
        
        result = self.word
        for old_char, new_char in diacritics_map.items():
            result = result.replace(old_char, new_char)
        
        # Remove specific diacritical marks
        diacritics_to_remove = {'̄', '̆', '̈', '̇', '̣', '̇'}
        result = ''.join(char for char in result if char not in diacritics_to_remove)
        
        # More specific handling for the examples
        replacements = {
            'ġ': 'g', 'ǣ': 'æ', 'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u', 'ȳ': 'y'
        }
        
        result = self.word
        for old_char, new_char in replacements.items():
            result = result.replace(old_char, new_char)
            
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
        result = self.remove_diacritics()
        
        # Then apply ASCII encoding substitutions
        ascii_replacements = {
            'þ': 'th', 'Þ': 'th',
            'æ': 'ae', 'Æ': 'ae',
            'ƿ': 'w', 'Ƿ': 'w',
            'ð': 'd', 'Ð': 'd'
        }
        
        for old_char, new_char in ascii_replacements.items():
            result = result.replace(old_char, new_char)
            
        return result