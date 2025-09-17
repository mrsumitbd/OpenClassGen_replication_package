class FieldPerm(object):
    '''
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
    '''

    def __init__(self, role_perms):
        self.role_perms = role_perms

    def get_perms(self, obj):
        '''
        Returns combined Environment's and object's permissions.
        Resulting condition is intersection of them.
        '''
        env_perms = self.available(obj)
        obj_perms = self.check(obj)
        return env_perms & obj_perms

    def available(self, field):
        '''
        Returns permissions according environment's limiting condition.
        Determined by object's context

        Allows only field's parents' permissions
        '''
        if hasattr(field, 'env') and hasattr(field.env, 'perms'):
            return set(field.env.perms)
        return set()

    def check(self, field):
        '''
        Returns permissions determined by object itself
        '''
        return set()

    def __repr__(self):
        return '<FieldPerm>'