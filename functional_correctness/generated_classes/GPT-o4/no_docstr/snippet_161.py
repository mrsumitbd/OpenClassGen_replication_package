class CallbackContainer(object):
    def __init__(self, client):
        self.client = client

    def messagePrint(self, client, userdata, message):
        try:
            text = message.payload.decode('utf-8')
        except Exception:
            text = message.payload
        print(f"Received on topic '{message.topic}': {text}")

    def messageForward(self, client, userdata, message):
        forward_topic = f"forward/{message.topic}"
        client.publish(forward_topic, message.payload, qos=message.qos)
        print(f"Forwarded message from '{message.topic}' to '{forward_topic}'")

    def pubackCallback(self, mid):
        print(f"Publish acknowledged, message ID: {mid}")

    def subackCallback(self, mid, data):
        print(f"Subscribe acknowledged, message ID: {mid}, granted QoS: {data}")