class _SchedulerCompatMixin(object):
    """
    Backwards compatibility helper for L{Scheduler} and L{SubScheduler}.

    This mixin provides all the attributes from L{IScheduler}, but provides
    them by adapting the L{Store} the item is in to L{IScheduler} and
    getting them from the resulting object.  Primarily in support of test
    code, it also supports rebinding those attributes by rebinding them on
    the L{IScheduler} powerup.

    @see: L{IScheduler}
    """

    @staticmethod
    def forwardToReal(name):
        def get(self):
            real = self.store.powerUp(IScheduler)
            return getattr(real, name)

        def set(self, value):
            real = self.store.powerUp(IScheduler)
            setattr(real, name, value)

        return property(get, set)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr in dir(IScheduler):
            if attr.startswith("_"):
                continue
            if hasattr(cls, attr):
                continue
            setattr(cls, attr, cls.forwardToReal(attr))

    def activate(self):
        """
        Whenever L{Scheduler} or L{SubScheduler} is created, either newly or
        when loaded from a database, emit a deprecation warning referring
        people to L{IScheduler}.
        """
        warn(
            "{} is deprecated; use IScheduler powerup on its Store instead."
            .format(self.__class__.__name__),
            DeprecationWarning,
            stacklevel=2
        )