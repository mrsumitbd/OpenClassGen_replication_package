class TornadoManager(object):

    def __init__(self):
        self.ioloops = {}
        self.threads = {}

    def add_ioloop(self, name, ioloop):
        self.ioloops[name] = ioloop

    def stop(self, name):
        if name in self.ioloops:
            ioloop = self.ioloops[name]
            ioloop.add_callback(ioloop.stop)
            if name in self.threads:
                self.threads[name].join()
                del self.threads[name]

    def start(self, name):
        if name in self.ioloops:
            ioloop = self.ioloops[name]
            thread = threading.Thread(target=ioloop.start)
            thread.daemon = True
            self.threads[name] = thread
            thread.start()

    def start_all(self):
        for name in self.ioloops:
            if name not in self.threads or not self.threads[name].is_alive():
                self.start(name)

    def stop_all(self):
        for name in list(self.ioloops.keys()):
            self.stop(name)