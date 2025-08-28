class CallbackContainer(object):

    def __init__(self, client):
        self.client = client
        self.callbacks = {}
        self.forward_topic = None
        self.forward_client = None

    def messagePrint(self, client, userdata, message):
        print(f"Topic: {message.topic}")
        print(f"Payload: {message.payload.decode('utf-8')}")
        print(f"QoS: {message.qos}")
        print(f"Retain: {message.retain}")

    def messageForward(self, client, userdata, message):
        if self.forward_client and self.forward_topic:
            self.forward_client.publish(self.forward_topic, message.payload, message.qos, message.retain)

    def pubackCallback(self, mid):
        if mid in self.callbacks:
            callback = self.callbacks.pop(mid)
            if callback:
                callback(mid)

    def subackCallback(self, mid, data):
        if mid in self.callbacks:
            callback = self.callbacks.pop(mid)
            if callback:
                callback(mid, data)