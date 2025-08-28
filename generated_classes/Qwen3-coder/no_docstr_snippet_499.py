class LaserBeam:
    def __init__(self):
        self.is_firing = False
        self.super_mode = False
        self.charge_level = 100

    def fire(self):
        if self.charge_level > 0:
            self.is_firing = True
            self.charge_level -= 10
            return "Laser beam fired!"
        else:
            return "Insufficient charge!"

    def activate_super(self):
        if self.charge_level >= 50:
            self.super_mode = True
            self.charge_level -= 50
            return "Super mode activated!"
        else:
            return "Not enough charge to activate super mode!"

    def destroy_planet(self):
        if self.super_mode and self.charge_level >= 100:
            self.charge_level = 0
            return "Planet destroyed!"
        else:
            return "Insufficient power to destroy planet!"