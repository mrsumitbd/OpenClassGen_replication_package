class DisableSignalling:
    '''
    Usage example:
    with DisableSignalling(cls.signal, self.slot):
        # do something
    pass
    '''

    def __init__(self, signal, slot):
        self.signal = signal
        self.slot = slot

    def __enter__(self):
        self.signal.disconnect(self.slot)
        return self

    def __exit__(self, type, value, traceback):
        self.signal.connect(self.slot)