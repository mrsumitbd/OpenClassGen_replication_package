class QueryCacheMiddleware(object):
    '''
    This middleware class monkey-patches django's ORM to maintain
    generational info on each table (model) and to automatically cache all
    querysets created via the ORM.  This should be the first middleware
    in your middleware stack.
    '''

    def __init__(self):
        self._patched = False
        self._original_methods = {}
        self._lock = threading.Lock()
        self._generations = {}
        self._patch_orm()

    def _patch_orm(self):
        if self._patched:
            return
            
        with self._lock:
            if self._patched:
                return
                
            # Store original methods
            self._original_methods['queryset_iterator'] = QuerySet.__iter__
            self._original_methods['queryset_count'] = QuerySet.count
            self._original_methods['queryset_exists'] = QuerySet.exists
            self._original_methods['model_save'] = models.Model.save
            self._original_methods['model_delete'] = models.Model.delete
            
            # Patch QuerySet methods
            QuerySet.__iter__ = self._cached_iterator
            QuerySet.count = self._cached_count
            QuerySet.exists = self._cached_exists
            
            # Patch Model methods to invalidate cache
            models.Model.save = self._invalidating_save
            models.Model.delete = self._invalidating_delete
            
            # Connect to bulk operations
            signals.post_save.connect(self._invalidate_model_cache)
            signals.post_delete.connect(self._invalidate_model_cache)
            
            self._patched = True

    def _get_cache_key(self, queryset):
        query_str = str(queryset.query)
        model_name = queryset.model._meta.label
        generation = self._get_generation(model_name)
        
        key_data = f"{model_name}:{generation}:{query_str}"
        return f"querycache:{hashlib.md5(key_data.encode()).hexdigest()}"

    def _get_generation(self, model_name):
        if model_name not in self._generations:
            self._generations[model_name] = cache.get(f"generation:{model_name}", 0)
        return self._generations[model_name]

    def _increment_generation(self, model_name):
        self._generations[model_name] = self._get_generation(model_name) + 1
        cache.set(f"generation:{model_name}", self._generations[model_name], None)

    def _cached_iterator(self, queryset):
        cache_key = self._get_cache_key(queryset)
        cached_result = cache.get(cache_key)
        
        if cached_result is not None:
            for item in cached_result:
                yield item
        else:
            result = list(QueryCacheMiddleware._original_methods['queryset_iterator'](queryset))
            cache.set(cache_key, result, 300)  # Cache for 5 minutes
            for item in result:
                yield item

    def _cached_count(self, queryset):
        cache_key = self._get_cache_key(queryset) + ":count"
        cached_result = cache.get(cache_key)
        
        if cached_result is not None:
            return cached_result
        else:
            result = QueryCacheMiddleware._original_methods['queryset_count'](queryset)
            cache.set(cache_key, result, 300)
            return result

    def _cached_exists(self, queryset):
        cache_key = self._get_cache_key(queryset) + ":exists"
        cached_result = cache.get(cache_key)
        
        if cached_result is not None:
            return cached_result
        else:
            result = QueryCacheMiddleware._original_methods['queryset_exists'](queryset)
            cache.set(cache_key, result, 300)
            return result

    def _invalidating_save(self, model_instance, *args, **kwargs):
        result = QueryCacheMiddleware._original_methods['model_save'](model_instance, *args, **kwargs)
        self._increment_generation(model_instance._meta.label)
        return result

    def _invalidating_delete(self, model_instance, *args, **kwargs):
        result = QueryCacheMiddleware._original_methods['model_delete'](model_instance, *args, **kwargs)
        self._increment_generation(model_instance._meta.label)
        return result

    def _invalidate_model_cache(self, sender, **kwargs):
        if hasattr(sender, '_meta'):
            self._increment_generation(sender._meta.label)

    def unpatch(self):
        if not self._patched:
            return
            
        with self._lock:
            if not self._patched:
                return
                
            # Restore original methods
            QuerySet.__iter__ = self._original_methods['queryset_iterator']
            QuerySet.count = self._original_methods['queryset_count']
            QuerySet.exists = self._original_methods['queryset_exists']
            models.Model.save = self._original_methods['model_save']
            models.Model.delete = self._original_methods['model_delete']
            
            # Disconnect signals
            signals.post_save.disconnect(self._invalidate_model_cache)
            signals.post_delete.disconnect(self._invalidate_model_cache)
            
            self._patched = False