class BaseEntrySearch(object):
    '''
    Mixin providing the behavior of the entry search view,
    by returning in the context the pattern searched, the
    error if something wrong has happened and finally the
    queryset of published entries matching the pattern.
    '''

    MIN_SEARCH_LENGTH = 3

    def get_queryset(self):
        '''
        Override the get_queryset method to
        do some validations and build the search queryset.
        '''
        qs = super(BaseEntrySearch, self).get_queryset()
        self.pattern = self.request.GET.get('pattern', '').strip()
        self.error = None

        if not self.pattern:
            self.error = 'Please enter a search term.'
            return qs.none()

        if len(self.pattern) < self.MIN_SEARCH_LENGTH:
            self.error = (
                f'Search term must be at least {self.MIN_SEARCH_LENGTH} characters.'
            )
            return qs.none()

        return qs.filter(
            published=True
        ).filter(
            Q(title__icontains=self.pattern) |
            Q(content__icontains=self.pattern)
        )

    def get_context_data(self, **kwargs):
        '''
        Add error and pattern in context.
        '''
        context = super(BaseEntrySearch, self).get_context_data(**kwargs)
        context['pattern'] = getattr(self, 'pattern', '')
        context['error'] = getattr(self, 'error', None)
        return context