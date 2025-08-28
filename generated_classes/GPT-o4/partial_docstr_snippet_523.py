class ConnectionConditions:
    '''
    Decorator for checking `connection` keys for existence or wait for them.
    Available options:

    :param fields: * `ConnectionConditions.user_required` — required "user"
          key, user already identified
        * `ConnectionConditions.login_required` — required "logged" key, user
          already logged in.
        * `ConnectionConditions.passive_server_started` — required
          "passive_server" key, user already send PASV and server awaits
          incomming connection
        * `ConnectionConditions.data_connection_made` — required "data_connection"
          key, user already connected to passive connection
        * `ConnectionConditions.rename_from_required` — required "rename_from"
          key, user already tell filename for rename

    :param wait: Indicates if should wait for parameters for
        `connection.wait_future_timeout`
    :type wait: :py:class:`bool`

    :param fail_code: return code if failure
    :type fail_code: :py:class:`str`

    :param fail_info: return information string if failure. If
        :py:class:`None`, then use default string
    :type fail_info: :py:class:`str`
    '''
    user_required = 1
    login_required = 2
    passive_server_started = 3
    data_connection_made = 4
    rename_from_required = 5

    _FIELD_NAMES = {
        user_required: "user",
        login_required: "logged",
        passive_server_started: "passive_server",
        data_connection_made: "data_connection",
        rename_from_required: "rename_from",
    }

    def __init__(self, *fields, wait=False, fail_code="503", fail_info=None):
        self.fields = fields
        self.wait = wait
        self.fail_code = fail_code
        self.fail_info = fail_info

    def __call__(self, f):
        @functools.wraps(f)
        async def wrapper(cls, connection, rest, *args):
            for field in self.fields:
                key = self._FIELD_NAMES.get(field)
                if key is None:
                    continue
                # wait for the key if requested
                if self.wait:
                    try:
                        await connection.wait_for(key, connection.wait_future_timeout)
                    except Exception:
                        info = self.fail_info or f"{key} required."
                        return self.fail_code, info
                else:
                    if not hasattr(connection, key):
                        info = self.fail_info or f"{key} required."
                        return self.fail_code, info
            return await f(cls, connection, rest, *args)
        return wrapper