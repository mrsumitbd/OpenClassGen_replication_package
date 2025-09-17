class Fruit:
    def __init__(self, name="fruit", color="unknown"):
        self.name = name
        self.color = color

    def __print_color(self, name, color):
        print(f"The {name} is {color}")

    def print(self):
        self.__print_color(self.name, self.color)