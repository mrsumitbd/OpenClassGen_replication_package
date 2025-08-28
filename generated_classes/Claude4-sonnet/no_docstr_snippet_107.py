class BumperClient:
    def __init__(self, ic, prefix, start=False):
        self.ic = ic
        self.prefix = prefix
        self.proxy = None
        self.bumper_data = None
        self.running = False
        
        if start:
            self.start()

    def start(self):
        if not self.running:
            try:
                proxy_string = self.prefix + ".Proxy"
                base = self.ic.stringToProxy(proxy_string)
                self.proxy = base.checkedCast(Ice.ObjectPrx)
                self.running = True
                self.bumper_data = {"left": False, "right": False, "front": False, "back": False}
            except Exception as e:
                self.running = False
                raise e

    def stop(self):
        if self.running:
            self.proxy = None
            self.running = False
            self.bumper_data = None

    def getBumperData(self):
        if self.running and self.proxy:
            try:
                # Simulate getting bumper data from the proxy
                return self.bumper_data
            except Exception as e:
                return None
        return None