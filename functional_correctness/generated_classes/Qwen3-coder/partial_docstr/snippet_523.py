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
        * `ConnectionConditions.data_connection_made` — required
          "data_connection" key, user already connected to passive connection
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

    ::

        >>> @ConnectionConditions(
        ...     ConnectionConditions.login_required,
        ...     ConnectionConditions.passive_server_started,
        ...     ConnectionConditions.data_connection_made,
        ...     wait=True)
        ... def foo(self, connection, rest):
        ...     ...
    '''

    user_required = "user"
    login_required = "logged"
    passive_server_started = "passive_server"
    data_connection_made = "data_connection"
    rename_from_required = "rename_from"

    def __init__(self, *fields, wait=False, fail_code="503", fail_info=None):
        self.fields = fields
        self.wait = wait
        self.fail_code = fail_code
        self.fail_info = fail_info

    def __call__(self, f):
        
        @functools.wraps(f)
        async def wrapper(cls, connection, rest, *args):
            for field in self.fields:
                if self.wait:
                    try:
                        await asyncio.wait_for(
                            connection.wait_future(field),
                            timeout=connection.wait_future_timeout
                        )
                    except asyncio.TimeoutError:
                        fail_info = self.fail_info or f"Required condition {field} not met"
                        return self.fail_code, fail_info
                else:
                    if field not in connection:
                        fail_info = self.fail_info or f"Required condition {field} not met"
                        return self.fail_code, fail_info
            
            return await f(cls, connection, rest, *args)
        
        return wrapper