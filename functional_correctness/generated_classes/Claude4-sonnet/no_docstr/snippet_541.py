class ResourceQuery:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.filters = []
        self.params = {}

    def filter(self, resource_manager, **params):
        self.resource_manager = resource_manager
        self.params.update(params)
        return self

    def _invoke_client_enum(self, client, enum_op, params, path):
        try:
            operation = getattr(client, enum_op)
            response = operation(**params)
            
            if path:
                result = response
                for key in path.split('.'):
                    if isinstance(result, dict):
                        result = result.get(key, [])
                    else:
                        result = getattr(result, key, [])
                return result
            
            return response
        except Exception as e:
            return []