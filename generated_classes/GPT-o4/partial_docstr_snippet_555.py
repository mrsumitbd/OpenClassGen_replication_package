class QueryCacheMiddleware(object):
    """
    This middleware class monkey-patches Django's ORM to maintain
    generational info on each table (model) and to automatically cache all
    querysets created via the ORM. This should be the first middleware
    in your middleware stack.
    """
    _cache = {}
    _generations = {}
    _patched = False
    _orig_fetch_all = None
    _invalidate = None

    def __init__(self):
        if not self.__class__._patched:
            # patch QuerySet._fetch_all
            self.__class__._orig_fetch_all = QuerySet._fetch_all

            def _patched_fetch_all(self):
                if self._result_cache is not None:
                    return
                sql, params = self.query.sql_with_params()
                tables = tuple(sorted(self.query.tables))
                gens = tuple(
                    (t, QueryCacheMiddleware._generations.get(t, 0))
                    for t in tables
                )
                key = (sql, params, gens)
                cache = QueryCacheMiddleware._cache
                if key in cache:
                    self._result_cache = cache[key]
                else:
                    QueryCacheMiddleware._orig_fetch_all(self)
                    cache[key] = list(self._result_cache)

            QuerySet._fetch_all = _patched_fetch_all

            # connect signals to invalidate on save/delete
            def invalidate(sender, **kwargs):
                table = sender._meta.db_table
                QueryCacheMiddleware._generations[table] = (
                    QueryCacheMiddleware._generations.get(table, 0) + 1
                )

            self.__class__._invalidate = invalidate
            signals.post_save.connect(invalidate)
            signals.post_delete.connect(invalidate)

            self.__class__._patched = True

    def unpatch(self):
        if not self.__class__._patched:
            return

        QuerySet._fetch_all = self.__class__._orig_fetch_all
        signals.post_save.disconnect(self.__class__._invalidate)
        signals.post_delete.disconnect(self.__class__._invalidate)

        self.__class__._patched = False
        QueryCacheMiddleware._cache.clear()
        QueryCacheMiddleware._generations.clear()