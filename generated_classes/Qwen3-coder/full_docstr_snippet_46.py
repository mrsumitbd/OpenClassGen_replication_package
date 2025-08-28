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
        if not request.user.is_active or not request.user.is_staff:
            return False
        if hasattr(request.user, 'otp_device') and request.user.otp_device:
            return True
        return False

    def login(self, request, extra_context=None):
        '''
        Redirects to the site login page for the given HttpRequest.
        '''
        from django.shortcuts import redirect
        from django.urls import reverse
        
        return redirect(reverse('admin:login'))