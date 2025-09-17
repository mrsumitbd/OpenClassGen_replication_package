class Pop3ContentLengthHandler(object):
    _LITERAL_RE = re.compile(r'\{(\d+)\+?\}$')

    def capacity(self):
        return sys.maxsize

    def encode(self, marionette_state, template, to_embed):
        """
        template should contain a '%d' placeholder where the length of to_embed goes.
        Returns a tuple of (command_string, to_embed_bytes).
        """
        size = len(to_embed)
        cmd = template % size
        return cmd, to_embed

    def decode(self, marionette_state, ctxt):
        """
        Reads a line from ctxt, detects a literal length {n} or {n+}, then reads n bytes
        plus the following CRLF, and returns the data block.
        If no literal marker is found, returns None.
        """
        line = ctxt.read_line()
        m = self._LITERAL_RE.search(line)
        if not m:
            return None
        length = int(m.group(1))
        data = ctxt.read(length)
        # consume the trailing CRLF after the data
        ctxt.read(2)
        return data