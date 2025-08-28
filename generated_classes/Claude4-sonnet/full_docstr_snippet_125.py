class BaseEntrySearch(object):
    '''
    Mixin providing the behavior of the entry search view,
    by returning in the context the pattern searched, the
    error if something wrong has happened and finally the
    the queryset of published entries matching the pattern.
    '''

    def get_queryset(self):
        '''
        Override the get_queryset method to
        do some validations and build the search queryset.
        '''
        queryset = super(BaseEntrySearch, self).get_queryset()
        self.pattern = ''
        self.error = None
        
        pattern = self.request.GET.get('pattern', '').strip()
        
        if not pattern:
            self.error = 'Please provide a search pattern'
            return queryset.none()
        
        if len(pattern) < 3:
            self.error = 'Search pattern must be at least 3 characters long'
            return queryset.none()
        
        self.pattern = pattern
        
        return queryset.filter(
            status='published'
        ).filter(
            models.Q(title__icontains=pattern) |
            models.Q(content__icontains=pattern) |
            models.Q(excerpt__icontains=pattern)
        ).distinct()

    def get_context_data(self, **kwargs):
        '''
        Add error and pattern in context.
        '''
        context = super(BaseEntrySearch, self).get_context_data(**kwargs)
        context['pattern'] = getattr(self, 'pattern', '')
        context['error'] = getattr(self, 'error', None)
        return context