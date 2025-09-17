class SemiMinorRadius:
    def __init__(self, value):
        self.value = float(value)

    def to_proj4(self):
        return f"+b={self.value}"

    def to_esri_wkt(self):
        return f"PARAMETER[\"Semi_Minor\",{self.value}]"

    def to_ogc_wkt(self):
        return f"PARAMETER[\"semi_minor\",{self.value}]"