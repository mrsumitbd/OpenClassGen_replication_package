class PDFGraphBackground(object):

    def __init__(self, background_style=None, border_size=None, background_border_color=None, background_fill_color=None, padding=0.0, stroke=None):
        self.background_style = background_style
        self.border_size = border_size
        self.background_border_color = background_border_color
        self.background_fill_color = background_fill_color
        self.padding = padding
        self.stroke = stroke

    @property
    def exists(self):
        return (self.background_style is not None or 
                self.border_size is not None or 
                self.background_border_color is not None or 
                self.background_fill_color is not None or 
                self.stroke is not None)