class FieldPerm(object):
    """
    Default permission getter for Field objects

    Ancestor should override the :meth:`check` method. They can use field.env
    to get any values from outside. For example::

        class RoleBased(FieldPerm):
            def __init__(self, role_perms):
                self.role_perms = role_perms

            def check(self, field):
                user = field.env.user
                perms = set(self.role_perms.get('*', ''))
                for role in user.roles:
                    perms.update(self.role_perms.get(role, ''))
                return perms
    """
    def __init__(self):
        super(FieldPerm, self).__init__()

    def get_perms(self, field):
        """
        Returns combined Environment's and object's permissions.
        Resulting condition is intersection of them.
        """
        # permissions determined by the object itself
        obj_perms = self.check(field) or set()

        # environment-level permissions: could be a dict, a callable, or a flat iterable
        env_perms = getattr(field.env, 'perms', {})
        if callable(env_perms):
            env_p = set(env_perms(field) or ())
        elif isinstance(env_perms, dict):
            # by field name, or '*' for default
            name = getattr(field, 'name', None)
            env_p = set(env_perms.get(name, env_perms.get('*', ())) or ())
        else:
            env_p = set(env_perms or ())

        return obj_perms & env_p

    def available(self, field):
        """
        Returns permissions according environment's limiting condition.
        Determined by object's context

        Allows only field's parents' permissions
        """
        # environment limiting condition
        env_limit = getattr(field.env, 'limit', {})
        if callable(env_limit):
            lim = set(env_limit(field) or ())
        elif isinstance(env_limit, dict):
            name = getattr(field, 'name', None)
            lim = set(env_limit.get(name, env_limit.get('*', ())) or ())
        else:
            lim = set(env_limit or ())

        # start with environment limit
        perms = lim
        # intersect with each parent's effective permissions
        for parent in getattr(field, 'parents', ()):
            perms &= self.get_perms(parent)

        return perms

    def check(self, field):
        """
        Returns permissions determined by object itself.
        Ancestors should override this.
        """
        return set()

    def __repr__(self):
        return '<%s>' % self.__class__.__name__