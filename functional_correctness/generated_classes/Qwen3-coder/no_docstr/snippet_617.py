class BinLine:
    def __init__(self, row):
        self.row = row

    def __str__(self):
        return str(self.row)

    def subtract(self, o):
        if len(self.row) != len(o.row):
            raise ValueError("Rows must have the same length")
        result = []
        for i in range(len(self.row)):
            result.append(self.row[i] - o.row[i])
        return BinLine(result)