class ResourceQuery:

    def __init__(self, session_factory):
        self._session_factory = session_factory

    def filter(self, resource_manager, **params):
        """
        Call the manager's enumeration operation and return all items.
        """
        # create a client/session from the factory
        client = self._session_factory()
        # invoke the enumeration and return a list
        return list(self._invoke_client_enum(
            client,
            resource_manager.enum_op,
            params,
            resource_manager.path
        ))

    def _invoke_client_enum(self, client, enum_op, params, path):
        """
        Invoke a client operation (with pagination if available), drill into
        the resulting structure by `path`, and yield each element.
        """
        # try to use a paginator if the client supports it
        try:
            paginator = client.get_paginator(enum_op)
        except Exception:
            paginator = None

        if paginator:
            pages = paginator.paginate(**params)
        else:
            operation = getattr(client, enum_op)
            pages = [operation(**params)]

        # for each page, walk down the nested keys and yield items
        for page in pages:
            data = page
            # allow path to be a string with dots or a list/tuple
            if isinstance(path, str):
                keys = path.split('.')
            else:
                keys = path

            for k in keys:
                data = data.get(k, {})

            if isinstance(data, list):
                for item in data:
                    yield item