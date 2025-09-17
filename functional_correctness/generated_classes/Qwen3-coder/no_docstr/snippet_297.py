class Api:
    def __init__(self, users, worker_ctx):
        self.users = users
        self.worker_ctx = worker_ctx
        self.current_user = None

    def authenticate(self, username, password):
        if username in self.users and self.users[username] == password:
            self.current_user = username
            return True
        return False

    def has_role(self, role):
        if self.current_user is None:
            return False
        # Assuming users dictionary structure includes roles
        # Example: {'username': {'password': 'pass', 'roles': ['admin', 'user']}}
        user_data = self.users.get(self.current_user, {})
        if isinstance(user_data, dict) and 'roles' in user_data:
            return role in user_data['roles']
        return False

    def check_role(self, role):
        if not self.has_role(role):
            raise PermissionError(f"User does not have required role: {role}")
        return True