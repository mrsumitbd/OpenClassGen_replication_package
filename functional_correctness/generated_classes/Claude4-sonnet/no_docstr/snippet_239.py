class CJsonSerializer(object):

    @classmethod
    def serialize(cls, data):
        return json.dumps(data)

    @classmethod
    def deserialize(cls, data):
        return json.loads(data)