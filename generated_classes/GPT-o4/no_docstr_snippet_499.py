class LaserBeam:
    def __init__(self):
        self.super_mode = False

    def fire(self):
        print("Firing laser beam.")

    def activate_super(self):
        if not self.super_mode:
            self.super_mode = True
            print("Super mode activated.")
        else:
            print("Super mode already active.")

    def destroy_planet(self):
        if self.super_mode:
            print("Planet destroyed!")
            self.super_mode = False
        else:
            print("Super mode not active. Cannot destroy planet.")