class ATFConverter:
    '''Class to convert tokens to unicode.

    Transliterates ATF data from CDLI into readable unicode.
        sz = š
        s, = ṣ
        t, = ṭ
        ' = ʾ
        Sign values for 2-3 take accent aigu and accent grave standards,
        otherwise signs are printed as subscript.

    For in depth reading on ATF-formatting for CDLI and ORACC:
        Oracc ATF Primer = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/index.html
        ATF Structure = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/structuretutorial/index.html
        ATF Inline = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/inlinetutorial/index.html
    '''

    def __init__(self, two_three: bool = True):
        '''
        :param two_three: turns on or off accent marking.
        '''
        self.two_three = two_three
        self.char_map = {
            'sz': 'š',
            's,': 'ṣ',
            't,': 'ṭ',
            "'": 'ʾ'
        }
        self.subscript_map = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
        }
        self.accent_map = {
            '2': 'á',
            '3': 'à'
        }

    def _convert_num(self, sign: str) -> str:
        '''
        Converts number registered in get_number_from_sign.
        '''
        match = re.search(r'(\d+)$', sign)
        if not match:
            return sign
        
        number = match.group(1)
        base = sign[:-len(number)]
        
        if self.two_three and number in ['2', '3'] and len(number) == 1:
            if base.endswith('a'):
                return base[:-1] + self.accent_map[number]
            else:
                return base + ''.join(self.subscript_map[d] for d in number)
        else:
            return base + ''.join(self.subscript_map[d] for d in number)

    def process(self, tokens: list[str]) -> list[str]:
        '''
        Expects a list of tokens, will return the list converted from ATF
        format to print-format.

        >>> c = ATFConverter()
        >>> c.process(["a", "a2", "a3", "geme2", "bad3", "buru14"])
        ['a', 'a₂', 'a₃', 'geme₂', 'bad₃', 'buru₁₄']
        '''
        result = []
        for token in tokens:
            converted = token
            
            # Apply character mappings
            for atf_char, unicode_char in self.char_map.items():
                converted = converted.replace(atf_char, unicode_char)
            
            # Convert numbers
            converted = self._convert_num(converted)
            
            result.append(converted)
        
        return result