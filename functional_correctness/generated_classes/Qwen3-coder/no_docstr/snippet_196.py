class TornadoManager(object):
    def __init__(self):
        self.ioloops = {}

    def add_ioloop(self, name, ioloop):
        self.ioloops[name] = ioloop

    def stop(self, name):
        if name in self.ioloops:
            self.ioloops[name].stop()

    def start(self, name):
        if name in self.ioloops:
            self.ioloops[name].start()

    def start_all(self):
        for ioloop in self.ioloops.values():
            ioloop.start()

    def stop_all(self):
        for ioloop in self.ioloops.values():
            ioloop.stop()