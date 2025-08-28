class AmazonTransport(object):
    def __init__(self, config):
        self.config = config
        self.is_running = False
        self.connection = None

    def startup(self):
        if not self.is_running:
            # Simulate connection establishment
            self.connection = f"Connected to Amazon transport with config: {self.config}"
            self.is_running = True
            return "Transport started successfully"
        return "Transport is already running"

    def deliver(self, message):
        if not self.is_running:
            raise RuntimeError("Transport is not running. Call startup() first.")
        
        if not message:
            raise ValueError("Message cannot be empty")
        
        # Simulate message delivery
        delivery_result = f"Message delivered: {message}"
        return delivery_result

    def shutdown(self):
        if self.is_running:
            # Simulate connection cleanup
            self.connection = None
            self.is_running = False
            return "Transport shut down successfully"
        return "Transport is not running"