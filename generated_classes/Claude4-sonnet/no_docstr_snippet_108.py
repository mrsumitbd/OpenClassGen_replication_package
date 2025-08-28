class vaex_evaluate_results_encoding:

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
            elif isinstance(result, (np.integer, np.floating)):
                return json.dumps({
                    'type': 'numpy_scalar',
                    'data': result.item(),
                    'dtype': str(result.dtype)
                })
            else:
                return json.dumps(result)
        elif encoding == 'arrow':
            import pyarrow as pa
            if isinstance(result, np.ndarray):
                array = pa.array(result)
                return base64.b64encode(array.to_pandas().to_numpy().tobytes()).decode('ascii')
            else:
                return base64.b64encode(pickle.dumps(result)).decode('ascii')
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")

    @classmethod
    def decode(cls, encoding, result_encoded):
        if encoding == 'pickle':
            return pickle.loads(base64.b64decode(result_encoded.encode('ascii')))
        elif encoding == 'json':
            data = json.loads(result_encoded)
            if isinstance(data, dict) and 'type' in data:
                if data['type'] == 'ndarray':
                    return np.array(data['data'], dtype=data['dtype']).reshape(data['shape'])
                elif data['type'] == 'numpy_scalar':
                    return np.array(data['data'], dtype=data['dtype']).item()
            return data
        elif encoding == 'arrow':
            try:
                import pyarrow as pa
                decoded_bytes = base64.b64decode(result_encoded.encode('ascii'))
                return np.frombuffer(decoded_bytes)
            except:
                return pickle.loads(base64.b64decode(result_encoded.encode('ascii')))
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")