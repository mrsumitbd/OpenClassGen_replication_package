class BinLine:
    def __init__(self, row):
        self.row = row

    def __str__(self):
        return ''.join(map(str, self.row))

    def subtract(self, o):
        result = []
        borrow = 0
        
        for i in range(len(self.row) - 1, -1, -1):
            diff = self.row[i] - o.row[i] - borrow
            
            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0
                
            result.append(diff)
        
        result.reverse()
        return BinLine(result)