class AdminSiteOTPRequiredMixin:
    '''
    Mixin for enforcing OTP verified staff users.

    Custom admin views should either be wrapped using :meth:`admin_view` or
    use :meth:`has_permission` in order to secure those views.
    '''

    def has_permission(self, request):
        '''
        Returns True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        '''
        # first check the normal admin permissions
        has_basic = False
        try:
            has_basic = super().has_permission(request)
        except AttributeError:
            user = getattr(request, 'user', None)
            has_basic = bool(user and user.is_active and user.is_staff)
        if not has_basic:
            return False

        user = request.user
        # superusers bypass OTP
        if user.is_superuser:
            return True
        # must have at least one OTP device
        if not user_has_device(user):
            return False
        # must have completed OTP verification in this session
        is_verified = getattr(user, 'is_verified', None)
        if callable(is_verified):
            return is_verified()
        return False

    def login(self, request, extra_context=None):
        '''
        Redirects to the site login page for the given HttpRequest.
        '''
        extra_context = extra_context.copy() if extra_context else {}
        extra_context['otp_required'] = True
        return super().login(request, extra_context)