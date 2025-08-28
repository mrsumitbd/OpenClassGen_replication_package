class ZoneStatus(object):
    def __init__(self, zone: int, power: bool, av: int, ir: int):
        self.zone = zone
        self.power = power
        self.av = av
        self.ir = ir

    @classmethod
    def from_string(cls, zone: int, string: str):
        """
        Expect string in the form "power,av,ir"
        where power is 0/1 or true/false/on/off,
        av and ir are integers.
        """
        parts = [p.strip() for p in string.split(",")]
        if len(parts) != 3:
            raise ValueError(f"Invalid input '{string}'; expected 3 comma‐separated values")
        p_str, av_str, ir_str = parts

        p_low = p_str.lower()
        if p_low in ("1", "true", "on", "yes"):
            power = True
        elif p_low in ("0", "false", "off", "no"):
            power = False
        else:
            raise ValueError(f"Cannot parse power value '{p_str}'")

        try:
            av = int(av_str)
        except ValueError:
            raise ValueError(f"Cannot parse av value '{av_str}' as int")

        try:
            ir = int(ir_str)
        except ValueError:
            raise ValueError(f"Cannot parse ir value '{ir_str}' as int")

        return cls(zone, power, av, ir)