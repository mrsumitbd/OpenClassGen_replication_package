class Page(object):

    def __init__(self, backend_document, width, height, rinoh_page):
        self.backend_document = backend_document
        self.width = width
        self.height = height
        self.rinoh_page = rinoh_page
        self.font_resources = {}

    def add_font_resource(self, font_name, font_rsc):
        if font_name in self.font_resources:
            return
        self.font_resources[font_name] = font_rsc
        if hasattr(self.backend_document, 'add_font'):
            try:
                self.backend_document.add_font(font_name, font_rsc)
            except TypeError:
                self.backend_document.add_font(font_rsc)
        if hasattr(self.rinoh_page, 'add_font_resource'):
            self.rinoh_page.add_font_resource(font_name, font_rsc)