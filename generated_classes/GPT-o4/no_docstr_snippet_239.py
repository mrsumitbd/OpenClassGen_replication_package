class CJsonSerializer(object):

    @classmethod
    def serialize(cls, data):
        """
        Serialize a Python object to a JSON-formatted string.
        """
        return json.dumps(data)

    @classmethod
    def deserialize(cls, data):
        """
        Deserialize a JSON-formatted string (or bytes) to a Python object.
        """
        if isinstance(data, (bytes, bytearray)):
            data = data.decode('utf-8')
        return json.loads(data)