class Phase:
    def __init__(self, duration, duration1, duration2, phaseDef):
        if not isinstance(duration, (int, float)):
            raise TypeError("duration must be a number")
        if not isinstance(duration1, (int, float)):
            raise TypeError("duration1 must be a number")
        if not isinstance(duration2, (int, float)):
            raise TypeError("duration2 must be a number")
        if duration1 + duration2 != duration:
            raise ValueError("duration1 + duration2 must equal duration")
        self.duration = duration
        self.duration1 = duration1
        self.duration2 = duration2
        self.phaseDef = phaseDef

    def __repr__(self):
        return (f"Phase(duration={self.duration}, "
                f"duration1={self.duration1}, "
                f"duration2={self.duration2}, "
                f"phaseDef={self.phaseDef!r})")