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

    _subscript_digits = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃',
        '4': '₄', '5': '₅', '6': '₆', '7': '₇',
        '8': '₈', '9': '₉'
    }
    _accent_map = {
        '2': '\u0301',  # combining acute
        '3': '\u0300'   # combining grave
    }

    def __init__(self, two_three: bool = True):
        '''
        :param two_three: turns on or off accent marking.
        '''
        self.two_three = two_three

    def _convert_num(self, sign: str) -> str:
        '''
        Converts number registered in get_number_from_sign.
        '''
        # If accent mapping is enabled for 2/3, use combining accent
        if not self.two_three and sign in ('2', '3'):
            return self._accent_map[sign]
        # Otherwise, map each digit to its subscript equivalent
        return ''.join(self._subscript_digits.get(d, '') for d in sign)

    def process(self, tokens: list[str]) -> list[str]:
        '''
        Expects a list of tokens, will return the list converted from ATF
        format to print-format.

        >>> c = ATFConverter()
        >>> c.process(["a", "a2", "a3", "geme2", "bad3", "buru14"])
        ['a', 'a₂', 'a₃', 'geme₂', 'bad₃', 'buru₁₄']
        '''
        out = []
        num_re = re.compile(r'(\d+)$')
        for tok in tokens:
            m = num_re.search(tok)
            if m:
                base, num = tok[:m.start()], m.group(1)
            else:
                base, num = tok, None
            # transliterate base
            base = base.replace('sz', 'š')
            base = base.replace('s,', 'ṣ')
            base = base.replace('t,', 'ṭ')
            base = base.replace("'", 'ʾ')
            if num:
                suffix = self._convert_num(num)
                out.append(base + suffix)
            else:
                out.append(base)
        return out