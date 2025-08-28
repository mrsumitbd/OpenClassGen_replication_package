class UserViewMixin(object):
    '''
    IMPORTANT: REQUIRES SaveHookMixin!

    This mixin alters a generic CREATE view that has a "created_by" field by
    automatically setting the user field to the current user when the form is
    submitted.
    The field name of the field to populate is specified by the user_field
    property and defaults to created_by.
    '''

    def __init__(self, *args, **kwargs):
        super(UserViewMixin, self).__init__(*args, **kwargs)
        if not hasattr(self, 'user_field'):
            self.user_field = 'created_by'

    def get_initial(self):
        '''
        Supply user object as initial data for the specified user_field(s).
        '''
        initial = super(UserViewMixin, self).get_initial()
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            if isinstance(self.user_field, (list, tuple)):
                for field in self.user_field:
                    initial[field] = self.request.user
            else:
                initial[self.user_field] = self.request.user
        return initial

    def pre_save(self, instance):
        super(UserViewMixin, self).pre_save(instance)
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            if isinstance(self.user_field, (list, tuple)):
                for field in self.user_field:
                    setattr(instance, field, self.request.user)
            else:
                setattr(instance, self.user_field, self.request.user)