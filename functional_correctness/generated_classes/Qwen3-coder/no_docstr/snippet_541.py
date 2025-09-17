class ResourceQuery:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def filter(self, resource_manager, **params):
        results = []
        session = self.session_factory()
        try:
            client = resource_manager.get_client(session)
            enum_op = resource_manager.get_enum_operation()
            path = resource_manager.get_path()
            results = self._invoke_client_enum(client, enum_op, params, path)
        finally:
            session.close()
        return results

    def _invoke_client_enum(self, client, enum_op, params, path):
        operation = getattr(client, enum_op)
        if params:
            return list(operation(**params))
        else:
            return list(operation())