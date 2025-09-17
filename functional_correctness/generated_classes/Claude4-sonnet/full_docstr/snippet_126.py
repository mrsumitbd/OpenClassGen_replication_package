class BaseEntryChannel(object):
    '''
    Mixin for displaying a custom selection of entries
    based on a search query, useful to build SEO/SMO pages
    aggregating entries on a thematic or for building a
    custom homepage.
    '''

    def get_queryset(self):
        '''
        Override the get_queryset method to build
        the queryset with entry matching query.
        '''
        queryset = super(BaseEntryChannel, self).get_queryset()
        query = getattr(self, 'query', None)
        if query:
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, **kwargs):
        '''
        Add query in context.
        '''
        context = super(BaseEntryChannel, self).get_context_data(**kwargs)
        context['query'] = getattr(self, 'query', None)
        return context