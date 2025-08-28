class Alignment:
    def __init__(self, s1: str, s2: str):
        self.s1 = s1
        self.s2 = s2
        self.matrix = [[None for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
        self.final_score = None

    def __str__(self) -> str:
        result = ""
        for i in range(len(self.s1) + 1):
            for j in range(len(self.s2) + 1):
                if self.matrix[i][j] is None:
                    result += "None\t"
                else:
                    result += f"({self.matrix[i][j][0]},{self.matrix[i][j][1]})\t"
            result += "\n"
        return result

    def get_entry(self, i: int, j: int):
        if 0 <= i <= len(self.s1) and 0 <= j <= len(self.s2):
            return self.matrix[i][j]
        return None

    def set_entry(self, i: int, j: int, score: int, pointer: int):
        if 0 <= i <= len(self.s1) and 0 <= j <= len(self.s2):
            self.matrix[i][j] = (score, pointer)
            if i == len(self.s1) and j == len(self.s2):
                self.final_score = score

    def get_score(self) -> int:
        return self.final_score