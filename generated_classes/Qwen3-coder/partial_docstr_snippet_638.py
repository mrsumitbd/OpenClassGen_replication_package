class _SchedulerCompatMixin(object):
    '''
    Backwards compatibility helper for L{Scheduler} and L{SubScheduler}.

    This mixin provides all the attributes from L{IScheduler}, but provides
    them by adapting the L{Store} the item is in to L{IScheduler} and
    getting them from the resulting object.  Primarily in support of test
    code, it also supports rebinding those attributes by rebinding them on
    the L{IScheduler} powerup.

    @see: L{IScheduler}
    '''

    def forwardToReal(name):
        def get(self):
            from twisted.internet.interfaces import IScheduler
            scheduler = IScheduler(self.store)
            return getattr(scheduler, name)

        def set(self, value):
            from twisted.internet.interfaces import IScheduler
            scheduler = IScheduler(self.store)
            setattr(scheduler, name, value)
        
        return property(get, set)

    def activate(self):
        '''
        Whenever L{Scheduler} or L{SubScheduler} is created, either newly or
        when loaded from a database, emit a deprecation warning referring
        people to L{IScheduler}.
        '''
        import warnings
        warnings.warn(
            "Scheduler and SubScheduler are deprecated. Use IScheduler instead.",
            DeprecationWarning,
            stacklevel=2
        )