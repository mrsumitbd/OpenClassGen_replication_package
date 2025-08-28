class Phase:
    def __init__(self, duration, duration1, duration2, phaseDef):
        self.duration = duration
        self.duration1 = duration1
        self.duration2 = duration2
        self.phaseDef = phaseDef

    def __repr__(self):
        return f"Phase(duration={self.duration}, duration1={self.duration1}, duration2={self.duration2}, phaseDef={self.phaseDef})"