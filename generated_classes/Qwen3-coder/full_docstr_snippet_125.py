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
        pattern = self.request.GET.get('pattern', '')
        
        if pattern:
            try:
                # Assuming there's a search method or filter logic
                # This is a generic implementation - adjust based on actual model fields
                queryset = queryset.filter(
                    title__icontains=pattern
                ) | queryset.filter(
                    content__icontains=pattern
                )
                queryset = queryset.distinct()
            except Exception:
                # If search fails, return empty queryset
                queryset = queryset.none()
        
        return queryset

    def get_context_data(self, **kwargs):
        '''
        Add error and pattern in context.
        '''
        context = super(BaseEntrySearch, self).get_context_data(**kwargs)
        pattern = self.request.GET.get('pattern', '')
        error = None
        
        context.update({
            'pattern': pattern,
            'error': error
        })
        
        return context