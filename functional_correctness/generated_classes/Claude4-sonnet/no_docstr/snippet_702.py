class PDFHtml(object):
    def __init__(self, parent, session, htmltext, formats=None, context=None):
        self.parent = parent
        self.session = session
        self.htmltext = htmltext
        self.formats = formats or {}
        self.context = context or {}
        self.parsed_content = []
        self._parsehtml()

    def _parsehtml(self):
        from html.parser import HTMLParser
        
        class PDFHTMLParser(HTMLParser):
            def __init__(self, pdf_html_instance):
                super().__init__()
                self.pdf_html = pdf_html_instance
                self.current_tag = None
                self.content_stack = []
                
            def handle_starttag(self, tag, attrs):
                self.current_tag = tag
                attr_dict = dict(attrs)
                self.content_stack.append({
                    'type': 'start_tag',
                    'tag': tag,
                    'attrs': attr_dict
                })
                
            def handle_endtag(self, tag):
                self.content_stack.append({
                    'type': 'end_tag',
                    'tag': tag
                })
                
            def handle_data(self, data):
                if data.strip():
                    self.content_stack.append({
                        'type': 'data',
                        'content': data.strip()
                    })
        
        parser = PDFHTMLParser(self)
        parser.feed(self.htmltext)
        self.parsed_content = parser.content_stack
        self._runlist(self.parsed_content)

    def _runlist(self, mylist):
        processed_items = []
        tag_stack = []
        
        for item in mylist:
            if item['type'] == 'start_tag':
                tag_stack.append(item['tag'])
                processed_items.append(item)
            elif item['type'] == 'end_tag':
                if tag_stack and tag_stack[-1] == item['tag']:
                    tag_stack.pop()
                processed_items.append(item)
            elif item['type'] == 'data':
                current_format = {}
                if tag_stack:
                    current_tag = tag_stack[-1]
                    if current_tag in self.formats:
                        current_format = self.formats[current_tag]
                
                processed_item = {
                    'type': 'formatted_data',
                    'content': item['content'],
                    'format': current_format,
                    'tags': tag_stack.copy()
                }
                processed_items.append(processed_item)
        
        self.processed_content = processed_items