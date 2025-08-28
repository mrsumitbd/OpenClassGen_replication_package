class AnimationClip(object):

    def __init__(self, tracks=None, fps=30, name=u"default"):
        self.tracks = tracks if tracks is not None else {}
        self.fps = fps
        self.name = name

    def set_property(self, frame, property, jstype, value):
        if property not in self.tracks:
            self.tracks[property] = {}
        
        self.tracks[property][frame] = {
            'type': jstype,
            'value': value
        }

    def lower(self):
        return self.name.lower()