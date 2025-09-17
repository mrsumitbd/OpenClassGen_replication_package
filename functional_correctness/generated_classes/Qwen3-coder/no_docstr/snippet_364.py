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
        return any(attr is not None for attr in [
            self.background_style,
            self.border_size,
            self.background_border_color,
            self.background_fill_color,
            self.padding,
            self.stroke
        ])