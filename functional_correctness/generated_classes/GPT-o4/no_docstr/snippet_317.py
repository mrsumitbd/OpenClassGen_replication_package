class SemiMinorRadius:
    def __init__(self, value):
        try:
            self.value = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid numeric value for semi‐minor radius: {value}")

    def to_proj4(self):
        # PROJ.4 parameter for semi‐minor axis is "+b="
        return f"+b={self.value}"

    def to_esri_wkt(self):
        # ESRI WKT uses PARAMETER["Semi_Minor_Axis", <value>]
        return f'PARAMETER["Semi_Minor_Axis",{self.value}]'

    def to_ogc_wkt(self):
        # OGC WKT uses lowercase parameter name "semi_minor"
        return f'PARAMETER["semi_minor",{self.value}]'