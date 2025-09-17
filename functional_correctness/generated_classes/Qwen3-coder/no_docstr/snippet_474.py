class Fruit:
    def __init__(self, vitamins):
        self.vitamins = vitamins

    def antioxidants(self):
        return f"This fruit contains vitamins: {', '.join(self.vitamins)}"