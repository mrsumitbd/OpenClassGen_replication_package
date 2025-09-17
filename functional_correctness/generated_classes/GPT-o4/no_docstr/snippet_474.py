class Fruit:
    def __init__(self, vitamins):
        self.vitamins = vitamins

    def antioxidants(self):
        return [v for v in self.vitamins if v in {"A", "C", "E"}]