class Alignment:
    def __init__(self, s1: str, s2: str):
        self.s1 = s1
        self.s2 = s2
        self.rows = len(s1) + 1
        self.cols = len(s2) + 1
        self.matrix = [[(0, 0) for _ in range(self.cols)] for _ in range(self.rows)]

    def __str__(self) -> str:
        result = []
        for i in range(self.rows):
            row_str = []
            for j in range(self.cols):
                score, pointer = self.matrix[i][j]
                row_str.append(f"({score},{pointer})")
            result.append(" ".join(row_str))
        return "\n".join(result)

    def get_entry(self, i: int, j: int):
        return self.matrix[i][j]

    def set_entry(self, i: int, j: int, score: int, pointer: int):
        self.matrix[i][j] = (score, pointer)

    def get_score(self) -> int:
        return self.matrix[self.rows - 1][self.cols - 1][0]