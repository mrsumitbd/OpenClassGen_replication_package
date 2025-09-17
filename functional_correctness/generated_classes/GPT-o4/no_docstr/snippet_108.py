class vaex_evaluate_results_encoding:

    @classmethod
    def encode(cls, encoding, result):
        if encoding in (None, 'none'):
            return result
        if encoding in ('pickle', 'binary'):
            return pickle.dumps(result)
        if encoding == 'json':
            def _encode(obj):
                if isinstance(obj, np.ndarray):
                    data = base64.b64encode(obj.tobytes()).decode('ascii')
                    return {'__ndarray__': True, 'data': data, 'dtype': str(obj.dtype), 'shape': obj.shape}
                if isinstance(obj, (np.integer,)):
                    return int(obj)
                if isinstance(obj, (np.floating,)):
                    return float(obj)
                if isinstance(obj, dict):
                    return {k: _encode(v) for k, v in obj.items()}
                if isinstance(obj, (list, tuple)):
                    return [_encode(v) for v in obj]
                return obj
            return json.dumps(_encode(result))
        raise ValueError(f"Unknown encoding: {encoding}")

    @classmethod
    def decode(cls, encoding, result_encoded):
        if encoding in (None, 'none'):
            return result_encoded
        if encoding in ('pickle', 'binary'):
            return pickle.loads(result_encoded)
        if encoding == 'json':
            def _decode(obj):
                if isinstance(obj, dict) and obj.get('__ndarray__'):
                    data = base64.b64decode(obj['data'])
                    arr = np.frombuffer(data, dtype=np.dtype(obj['dtype']))
                    return arr.reshape(obj['shape'])
                if isinstance(obj, dict):
                    return {k: _decode(v) for k, v in obj.items()}
                if isinstance(obj, list):
                    return [_decode(v) for v in obj]
                return obj
            return _decode(json.loads(result_encoded))
        raise ValueError(f"Unknown encoding: {encoding}")