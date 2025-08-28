class Page(object):
    def __init__(self, backend_document, width, height, rinoh_page):
        self.backend_document = backend_document
        self.width = width
        self.height = height
        self.rinoh_page = rinoh_page
        self.font_resources = {}

    def add_font_resource(self, font_name, font_rsc):
        self.font_resources[font_name] = font_rsc