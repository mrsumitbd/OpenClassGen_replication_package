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
        self.replacements = {
            'sz': 'š',
            's,': 'ṣ',
            't,': 'ṭ',
            "'": 'ʾ'
        }

    def _convert_num(self, sign: str) -> str:
        '''
        Converts number registered in get_number_from_sign.
        '''
        if not sign:
            return ''
        
        num = int(sign)
        if self.two_three:
            if num == 2:
                return '́'  # Combining acute accent
            elif num == 3:
                return '̀'  # Combining grave accent
        
        # Convert to subscript numbers
        subscript_map = {
            '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
            '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
        }
        return ''.join(subscript_map.get(digit, digit) for digit in str(num))

    def process(self, tokens: list[str]) -> list[str]:
        '''
        Expects a list of tokens, will return the list converted from ATF
        format to print-format.

        >>> c = ATFConverter()
        >>> c.process(["a", "a2", "a3", "geme2", "bad3", "buru14"])
        ['a', 'a₂', 'a₃', 'geme₂', 'bad₃', 'buru₁₄']
        '''
        import re
        
        result = []
        
        for token in tokens:
            # Apply character replacements first
            converted_token = token
            for atf_char, unicode_char in self.replacements.items():
                converted_token = converted_token.replace(atf_char, unicode_char)
            
            # Handle numbers in the token
            # Find all sequences of digits
            def replace_numbers(match):
                number = match.group()
                return self._convert_num(number)
            
            # Replace digits that are not part of a larger alphanumeric sequence
            # This regex looks for digits that may be at the beginning, middle, or end
            converted_token = re.sub(r'\d+', replace_numbers, converted_token)
            
            result.append(converted_token)
        
        return result