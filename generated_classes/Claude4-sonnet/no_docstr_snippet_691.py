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
        parts = string.strip().split()
        power = parts[0].lower() == 'on' if len(parts) > 0 else False
        av = int(parts[1]) if len(parts) > 1 else 0
        ir = int(parts[2]) if len(parts) > 2 else 0
        return cls(zone, power, av, ir)