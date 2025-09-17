class Fruit:
    def __init__(self, vitamins):
        self.vitamins = vitamins

    def antioxidants(self):
        return sum(self.vitamins.values())