class PopulateResponseMixin:
    @classmethod
    def from_response(cls, raw_response):
        if hasattr(raw_response, 'json') and callable(raw_response.json):
            data = raw_response.json()
        else:
            data = raw_response

        if isinstance(data, str):
            data = json.loads(data)

        if not isinstance(data, dict):
            raise ValueError(f"Expected dict or JSON response, got {type(data).__name__}")

        instance = cls(**data)
        setattr(instance, 'raw_response', raw_response)
        return instance