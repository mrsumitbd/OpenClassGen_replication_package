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
        from django_otp import user_has_device
        from django_otp.decorators import otp_required
        
        has_basic_permission = super().has_permission(request)
        if not has_basic_permission:
            return False
            
        if not request.user.is_authenticated:
            return False
            
        if not user_has_device(request.user):
            return False
            
        return request.user.is_verified()

    def login(self, request, extra_context=None):
        '''
        Redirects to the site login page for the given HttpRequest.
        '''
        from django.contrib.auth.views import redirect_to_login
        from django.urls import reverse
        from django_otp import user_has_device
        
        if request.user.is_authenticated and request.user.is_staff:
            if user_has_device(request.user) and not request.user.is_verified():
                return redirect_to_login(
                    request.get_full_path(),
                    reverse('two_factor:login')
                )
        
        return super().login(request, extra_context)