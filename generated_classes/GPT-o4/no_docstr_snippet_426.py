class Fruit:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __print_color(self, name, color):
        print(f"{name} is {color}")

    def print(self):
        self.__print_color(self.name, self.color)