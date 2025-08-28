class Encoder:
    '''
    An XML special character encoder/decoder.
    @cvar encodings: A mapping of special characters encoding.
    @type encodings: [(str,str)]
    @cvar decodings: A mapping of special characters decoding.
    @type decodings: [(str,str)]
    @cvar special: A list of special characters
    @type special: [char]
    '''
    encodings = [
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ('"', "&quot;"),
        ("'", "&apos;")
    ]
    decodings = [(ent, ch) for ch, ent in encodings]
    special = [ch for ch, _ in encodings]

    def needsEncoding(self, s):
        '''
            Get whether string I{s} contains special characters.
            @param s: A string to check.
            @type s: str
            @return: True if needs encoding.
            @rtype: boolean
        '''
        return any(c in s for c in self.special)

    def encode(self, s):
        '''
            Encode special characters found in string I{s}.
            @param s: A string to encode.
            @type s: str
            @return: The encoded string.
            @rtype: str
        '''
        result = s
        # encode '&' first to avoid double-encoding
        for ch, ent in self.encodings:
            result = result.replace(ch, ent)
        return result

    def decode(self, s):
        '''
            Decode special characters encodings found in string I{s}.
            @param s: A string to decode.
            @type s: str
            @return: The decoded string.
            @rtype: str
        '''
        result = s
        # decode longer entities first to avoid partial replacements
        for ent, ch in sorted(self.decodings, key=lambda x: -len(x[0])):
            result = result.replace(ent, ch)
        return result