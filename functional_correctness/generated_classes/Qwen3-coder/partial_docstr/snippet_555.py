class QueryCacheMiddleware(object):
    '''
    This middleware class monkey-patches django's ORM to maintain
    generational info on each table (model) and to automatically cache all
    querysets created via the ORM.  This should be the first middleware
    in your middleware stack.
    '''

    def __init__(self):
        self.patched = False
        self.original_manager = None
        self.original_queryset = None

    def unpatch(self):
        if not self.patched:
            return
            
        # Restore original Django ORM methods
        if self.original_manager:
            import django.db.models.manager
            django.db.models.manager.Manager.get_queryset = self.original_manager
            
        if self.original_queryset:
            import django.db.models.query
            django.db.models.query.QuerySet.__iter__ = self.original_queryset
            
        self.patched = False