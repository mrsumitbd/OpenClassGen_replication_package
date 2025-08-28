class Api:
    def __init__(self, users, worker_ctx):
        self.users = users
        self.worker_ctx = worker_ctx
        self.current_user = None

    def authenticate(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = self.users[username]
            self.current_user['username'] = username
            return True
        return False

    def has_role(self, role):
        if self.current_user is None:
            return False
        return role in self.current_user.get('roles', [])

    def check_role(self, role):
        if not self.has_role(role):
            raise PermissionError(f"User does not have required role: {role}")
        return True