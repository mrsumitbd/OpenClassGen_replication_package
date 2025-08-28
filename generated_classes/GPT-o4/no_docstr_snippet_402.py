class Alignment:

    def __init__(self, s1: str, s2: str):
        self.s1 = s1
        self.s2 = s2
        # matrix of (score, pointer) tuples
        self.matrix = [
            [(None, None) for _ in range(len(s2) + 1)]
            for _ in range(len(s1) + 1)
        ]

    def __str__(self) -> str:
        # header row
        cols = ["  "] + list(self.s2)
        header = "  ".join(cols)
        lines = [header]
        # each row
        for i, row in enumerate(self.matrix):
            label = self.s1[i - 1] if i > 0 else " "
            entries = []
            for score, ptr in row:
                s = str(score) if score is not None else "."
                p = str(ptr) if ptr is not None else "."
                entries.append(f"{s},{p}")
            lines.append(label + " " + " ".join(entries))
        return "\n".join(lines)

    def get_entry(self, i: int, j: int):
        if i < 0 or j < 0 or i > len(self.s1) or j > len(self.s2):
            raise IndexError("Alignment indices out of range")
        return self.matrix[i][j]

    def set_entry(self, i: int, j: int, score: int, pointer: int):
        if i < 0 or j < 0 or i > len(self.s1) or j > len(self.s2):
            raise IndexError("Alignment indices out of range")
        self.matrix[i][j] = (score, pointer)

    def get_score(self) -> int:
        sc, _ = self.matrix[len(self.s1)][len(self.s2)]
        return sc