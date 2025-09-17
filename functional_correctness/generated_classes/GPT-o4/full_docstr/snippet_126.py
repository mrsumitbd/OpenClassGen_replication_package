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
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(body__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        '''
        Add query in context.
        '''
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        return context