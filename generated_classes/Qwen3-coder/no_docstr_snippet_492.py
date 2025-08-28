class vaex_task_result_encoding:
    @classmethod
    def encode(cls, encoding, result):
        if encoding == 'json':
            import json
            return json.dumps(result)
        elif encoding == 'pickle':
            import pickle
            return pickle.dumps(result)
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")

    @classmethod
    def decode(cls, encoding, result_encoded):
        if encoding == 'json':
            import json
            return json.loads(result_encoded)
        elif encoding == 'pickle':
            import pickle
            return pickle.loads(result_encoded)
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")