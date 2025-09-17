class SemiMinorRadius:
    def __init__(self, value):
        self.value = value

    def to_proj4(self):
        return f"+b={self.value}"

    def to_esri_wkt(self):
        return f'SEMI_MINOR_RADIUS[{self.value}]'

    def to_ogc_wkt(self):
        return f'SEMI_MINOR_RADIUS[{self.value}]'