class _FileContext(object):
    def __init__(self, sourcepath, streamerinfos, streamerinfosmap, classes, compression, tfile):
        self.sourcepath = sourcepath
        self.streamerinfos = list(streamerinfos)
        self.streamerinfosmap = dict(streamerinfosmap)
        self.classes = list(classes)
        self.compression = compression
        self.tfile = tfile

    def copy(self):
        return _FileContext(
            self.sourcepath,
            copy.deepcopy(self.streamerinfos),
            copy.deepcopy(self.streamerinfosmap),
            copy.deepcopy(self.classes),
            self.compression,
            self.tfile
        )