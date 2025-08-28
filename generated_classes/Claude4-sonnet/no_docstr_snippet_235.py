class _FileContext(object):

    def __init__(self, sourcepath, streamerinfos, streamerinfosmap, classes, compression, tfile):
        self.sourcepath = sourcepath
        self.streamerinfos = streamerinfos
        self.streamerinfosmap = streamerinfosmap
        self.classes = classes
        self.compression = compression
        self.tfile = tfile

    def copy(self):
        return _FileContext(
            self.sourcepath,
            self.streamerinfos,
            self.streamerinfosmap,
            self.classes,
            self.compression,
            self.tfile
        )