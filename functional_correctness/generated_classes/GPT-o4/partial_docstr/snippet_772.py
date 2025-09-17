class UserViewMixin(object):
    """
    IMPORTANT: REQUIRES SaveHookMixin!

    This mixin alters a generic CREATE view that has a "created_by" field by
    automatically setting the user field to the current user when the form is
    submitted.
    The field name of the field to populate is specified by the user_field
    property and defaults to created_by.
    """
    user_field = 'created_by'

    def __init__(self, *args, **kwargs):
        super(UserViewMixin, self).__init__(*args, **kwargs)

    def get_initial(self):
        """
        Supply user object as initial data for the specified user_field(s).
        """
        # Start with any initial data from parent
        try:
            initial = super(UserViewMixin, self).get_initial() or {}
        except AttributeError:
            initial = {}

        # Normalize to a list of field names
        fields = (self.user_field
                  if isinstance(self.user_field, (list, tuple))
                  else [self.user_field])

        for fld in fields:
            initial[fld] = self.request.user

        return initial

    def pre_save(self, instance):
        """
        Hook called by SaveHookMixin just before saving the instance.
        """
        # Normalize to a list of field names
        fields = (self.user_field
                  if isinstance(self.user_field, (list, tuple))
                  else [self.user_field])

        for fld in fields:
            setattr(instance, fld, self.request.user)

        return instance