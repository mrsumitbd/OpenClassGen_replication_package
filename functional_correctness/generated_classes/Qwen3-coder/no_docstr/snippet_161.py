class CallbackContainer(object):
    def __init__(self, client):
        self.client = client
        self.message_handlers = []

    def messagePrint(self, client, userdata, message):
        print(f"Received message on topic {message.topic}: {message.payload.decode()}")

    def messageForward(self, client, userdata, message):
        # Forward message to all registered handlers
        for handler in self.message_handlers:
            try:
                handler(client, userdata, message)
            except Exception as e:
                print(f"Error in message handler: {e}")

    def pubackCallback(self, mid):
        print(f"Publish acknowledged for message ID: {mid}")

    def subackCallback(self, mid, data):
        print(f"Subscribe acknowledged for message ID: {mid}, QoS levels: {data}")