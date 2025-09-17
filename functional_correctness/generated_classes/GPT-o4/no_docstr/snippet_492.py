class vaex_task_result_encoding:

    @classmethod
    def encode(cls, encoding, result):
        if encoding is None or encoding == 'raw':
            return result

        if encoding == 'pickle':
            # serialize any Python object to bytes
            return pickle.dumps(result)

        if encoding == 'base64':
            # pickle, then base64-encode to ASCII string
            data = pickle.dumps(result)
            return base64.b64encode(data).decode('ascii')

        if encoding == 'json':
            # JSON-serialize; convert numpy arrays to lists
            def _default(o):
                if isinstance(o, np.ndarray):
                    return o.tolist()
                raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")
            return json.dumps(result, default=_default)

        if encoding == 'ndarray_binary':
            # efficient binary encoding for numpy arrays
            if not isinstance(result, np.ndarray):
                raise ValueError("ndarray_binary encoding requires a numpy.ndarray")
            payload = {
                "__array__": True,
                "dtype": str(result.dtype),
                "shape": result.shape,
                "data": base64.b64encode(result.tobytes()).decode('ascii')
            }
            return payload

        raise ValueError(f"Unknown encoding: {encoding!r}")

    @classmethod
    def decode(cls, encoding, result_encoded):
        if encoding is None or encoding == 'raw':
            return result_encoded

        if encoding == 'pickle':
            # deserialize from bytes
            return pickle.loads(result_encoded)

        if encoding == 'base64':
            # base64-decode then unpickle
            data = base64.b64decode(result_encoded)
            return pickle.loads(data)

        if encoding == 'json':
            # JSON-deserialize; numpy arrays remain lists
            return json.loads(result_encoded)

        if encoding == 'ndarray_binary':
            # reconstruct numpy array
            if not (isinstance(result_encoded, dict) and result_encoded.get("__array__")):
                raise ValueError("Invalid ndarray_binary payload")
            dtype = np.dtype(result_encoded["dtype"])
            shape = tuple(result_encoded["shape"])
            raw = base64.b64decode(result_encoded["data"])
            array = np.frombuffer(raw, dtype=dtype)
            return array.reshape(shape)

        raise ValueError(f"Unknown encoding: {encoding!r}")