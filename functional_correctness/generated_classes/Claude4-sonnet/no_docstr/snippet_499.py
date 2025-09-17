class LaserBeam:
    def __init__(self):
        self.power_level = 1
        self.is_active = False
        self.super_mode = False
        self.charge = 0
        self.max_charge = 100

    def fire(self):
        if self.is_active and self.charge >= 10:
            self.charge -= 10
            damage = self.power_level * 10
            if self.super_mode:
                damage *= 5
            return damage
        return 0

    def activate_super(self):
        if self.charge >= 50:
            self.super_mode = True
            self.is_active = True
            self.charge -= 50
            self.power_level *= 3
            return True
        return False

    def destroy_planet(self):
        if self.super_mode and self.charge >= 80:
            self.charge = 0
            self.super_mode = False
            self.power_level = 1
            self.is_active = False
            return "Planet destroyed!"
        return "Insufficient power to destroy planet"