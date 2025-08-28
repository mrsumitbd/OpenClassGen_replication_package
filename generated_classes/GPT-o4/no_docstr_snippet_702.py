class PDFHtml(object):

    def __init__(self, parent, session, htmltext, formats=None, context=None):
        self.parent = parent
        self.session = session
        self.htmltext = htmltext or ''
        self.formats = formats or {}
        self.context = context or {}

    def _parsehtml(self):
        class _Parser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.commands = []

            def handle_starttag(self, tag, attrs):
                self.commands.append(('start', tag, dict(attrs)))

            def handle_endtag(self, tag):
                self.commands.append(('end', tag))

            def handle_data(self, data):
                if data:
                    self.commands.append(('data', data))

        p = _Parser()
        p.feed(self.htmltext)
        return p.commands

    def _runlist(self, mylist):
        c = self.parent
        lh = self.formats.get('line_height', 10)
        psp = self.formats.get('p_spacing', lh)
        for cmd in mylist:
            kind = cmd[0]
            if kind == 'start':
                tag, attrs = cmd[1], cmd[2]
                if tag in ('b', 'strong'):
                    c.set_font(style='B')
                elif tag in ('i', 'em'):
                    c.set_font(style='I')
                elif tag == 'u':
                    c.set_font(style='', underline=True)
                elif tag == 'br':
                    c.ln(lh)
                elif tag == 'p':
                    c.ln(psp)
                elif tag == 'img':
                    src = attrs.get('src', '')
                    w = attrs.get('width')
                    h = attrs.get('height')
                    try:
                        w = float(w) if w else None
                        h = float(h) if h else None
                    except:
                        w = h = None
                    c.image(src, w=w, h=h)
            elif kind == 'end':
                tag = cmd[1]
                if tag in ('b', 'strong', 'i', 'em', 'u'):
                    c.set_font(style='')
                elif tag == 'p':
                    c.ln(psp)
            elif kind == 'data':
                text = _html.unescape(cmd[1])
                if '\n' in text:
                    c.multi_cell(0, lh, text)
                else:
                    c.write(lh, text)