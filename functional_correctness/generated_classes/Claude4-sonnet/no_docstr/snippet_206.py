class PopulateResponseMixin:
    @classmethod
    def from_response(cls, raw_response):
        instance = cls()
        
        if hasattr(raw_response, 'json'):
            try:
                data = raw_response.json()
            except (ValueError, AttributeError):
                data = {}
        elif isinstance(raw_response, dict):
            data = raw_response
        else:
            try:
                import json
                data = json.loads(raw_response)
            except (ValueError, TypeError):
                data = {}
        
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        return instance