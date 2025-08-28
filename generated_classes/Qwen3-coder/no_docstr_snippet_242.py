class AnimationClip(object):
    def __init__(self, tracks=None, fps=30, name=u"default"):
        self.tracks = tracks if tracks is not None else {}
        self.fps = fps
        self.name = name

    def set_property(self, frame, property, jstype, value):
        if frame not in self.tracks:
            self.tracks[frame] = {}
        if property not in self.tracks[frame]:
            self.tracks[frame][property] = {}
        self.tracks[frame][property][jstype] = value

    def lower(self):
        return {
            "tracks": self.tracks,
            "fps": self.fps,
            "name": self.name
        }