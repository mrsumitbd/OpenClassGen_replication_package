class AnimationClip(object):

    def __init__(self, tracks=None, fps=30, name=u"default"):
        self.tracks = {} if tracks is None else tracks
        self.fps = fps
        self.name = name

    def set_property(self, frame, property, jstype, value):
        if property not in self.tracks:
            self.tracks[property] = {}
        if jstype not in self.tracks[property]:
            self.tracks[property][jstype] = []
        self.tracks[property][jstype].append({
            'frame': frame,
            'value': value
        })

    def lower(self):
        output = {
            'name': self.name,
            'fps': self.fps,
            'tracks': []
        }
        for prop, jsmap in self.tracks.items():
            for jstype, keylist in jsmap.items():
                sorted_keys = sorted(keylist, key=lambda k: k['frame'])
                output['tracks'].append({
                    'property': prop,
                    'type': jstype,
                    'keys': sorted_keys
                })
        return output