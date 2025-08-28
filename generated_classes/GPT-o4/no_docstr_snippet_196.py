class TornadoManager(object):
    def __init__(self):
        self._loops = {}

    def add_ioloop(self, name, ioloop):
        if name in self._loops:
            raise ValueError("IOLoop with name '{}' already exists".format(name))
        self._loops[name] = {'loop': ioloop, 'thread': None}

    def start(self, name):
        if name not in self._loops:
            raise KeyError("No IOLoop named '{}'".format(name))
        info = self._loops[name]
        thread = info['thread']
        if thread and thread.is_alive():
            return
        t = threading.Thread(target=info['loop'].start, name='IOLoop-{}'.format(name))
        t.daemon = True
        info['thread'] = t
        t.start()

    def stop(self, name):
        if name not in self._loops:
            raise KeyError("No IOLoop named '{}'".format(name))
        info = self._loops[name]
        info['loop'].stop()
        t = info['thread']
        if t:
            t.join()
            info['thread'] = None

    def start_all(self):
        for name in self._loops:
            self.start(name)

    def stop_all(self):
        for name in self._loops:
            self.stop(name)