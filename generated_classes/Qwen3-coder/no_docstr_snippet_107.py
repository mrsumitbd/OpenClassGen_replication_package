class BumperClient:
    def __init__(self, ic, prefix, start=False):
        self.ic = ic
        self.prefix = prefix
        self.bumper_data = None
        self.running = False
        
        if start:
            self.start()

    def start(self):
        if not self.running:
            # Simulate starting the bumper client
            self.running = True
            # In a real implementation, this would connect to hardware or simulation
            self.bumper_data = {"left": False, "right": False, "front": False}

    def stop(self):
        if self.running:
            self.running = False
            self.bumper_data = None

    def getBumperData(self):
        if self.running and self.bumper_data is not None:
            return self.bumper_data
        else:
            return {"left": False, "right": False, "front": False}