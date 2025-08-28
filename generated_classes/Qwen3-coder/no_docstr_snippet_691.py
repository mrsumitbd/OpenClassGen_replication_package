class ZoneStatus(object):
    def __init__(self,
                 zone: int,
                 power: bool,
                 av: int,
                 ir: int):
        self.zone = zone
        self.power = power
        self.av = av
        self.ir = ir

    @classmethod
    def from_string(cls, zone: int, string: str):
        parts = string.split(',')
        power = parts[0].strip() == 'ON'
        av = int(parts[1].strip())
        ir = int(parts[2].strip())
        return cls(zone, power, av, ir)