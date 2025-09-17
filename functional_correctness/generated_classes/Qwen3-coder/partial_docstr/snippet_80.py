class OneTrackMind(object):
    '''An accurate simulation of my brain

    I can know one thing at a time, at some level of confidence. You can tell
    me other things, but if I'm not as confident of them, I'll forget them. If
    I'm more confident of them, they'll replace what I knew before.

    '''

    def __init__(self):
        self._knowledge = None
        self._confidence = 0.0

    def know(self, what, confidence):
        '''Know something with the given confidence, and return self for chaining.

        If confidence is higher than that of what we already know, replace
        what we already know with what you're telling us.

        '''
        if confidence > self._confidence:
            self._knowledge = what
            self._confidence = confidence
        return self