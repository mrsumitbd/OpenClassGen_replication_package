class Api:

    def __init__(self, users, worker_ctx):
        self._users = users
        self._ctx = worker_ctx
        setattr(self._ctx, 'user', None)

    def authenticate(self, username, password):
        user = self._users.get(username)
        if user is None or user.get('password') != password:
            raise ValueError("Invalid username or password")
        setattr(self._ctx, 'user', username)

    def has_role(self, role):
        current = getattr(self._ctx, 'user', None)
        if current is None:
            return False
        return role in self._users.get(current, {}).get('roles', [])

    def check_role(self, role):
        if not self.has_role(role):
            raise PermissionError(f"Access denied, missing role: {role}")