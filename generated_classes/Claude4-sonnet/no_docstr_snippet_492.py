class vaex_task_result_encoding:

    @classmethod
    def encode(cls, encoding, result):
        if encoding == 'pickle':
            return base64.b64encode(pickle.dumps(result)).decode('ascii')
        elif encoding == 'json':
            if isinstance(result, np.ndarray):
                return json.dumps({
                    'type': 'ndarray',
                    'data': result.tolist(),
                    'dtype': str(result.dtype),
                    'shape': result.shape
                })
            else:
                return json.dumps(result)
        elif encoding == 'raw':
            return result
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")

    @classmethod
    def decode(cls, encoding, result_encoded):
        if encoding == 'pickle':
            return pickle.loads(base64.b64decode(result_encoded.encode('ascii')))
        elif encoding == 'json':
            decoded = json.loads(result_encoded)
            if isinstance(decoded, dict) and decoded.get('type') == 'ndarray':
                return np.array(decoded['data'], dtype=decoded['dtype']).reshape(decoded['shape'])
            else:
                return decoded
        elif encoding == 'raw':
            return result_encoded
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")