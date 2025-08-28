class AstromData(object):
    """
    Encapsulates data extracted from an .astrom file.
    """

    def __init__(self, observations, sys_header, sources, discovery_only=False):
        """
        Constructs a new astronomy data set object.

        Args:
          observations: list(Observations)
            The observations that are part of the data set.
          sys_header: dict
            Key-value pairs of system settings applicable to the data set.
            Ex: RMIN, RMAX, ANGLE, AWIDTH
          sources: list(list(SourceReading))
            A list of point sources found in the data set.  These are
            potential moving objects.  Each point source is itself a list
            of source readings, one for each observation in
            <code>observations</code>.  By convention the ordering of
            source readings must match the ordering of the observations.
          discovery_only: bool
            should we only use the discovery images on the first pass?
        """
        self.observations = list(observations)
        self.sys_header = dict(sys_header)
        # each source is a list of readings
        self._all_sources = [list(src) for src in sources]
        self.discovery_only = bool(discovery_only)

    def get_reading_count(self):
        """
        Returns the total number of readings across sources,
        honoring discovery_only if set.
        """
        return sum(len(src) for src in self.get_sources())

    def get_sources(self):
        """
        Returns the list of sources (each a list of readings).
        If discovery_only is True, returns only the first reading of each source.
        """
        if self.discovery_only:
            return [src[:1] for src in self._all_sources if src]
        return list(self._all_sources)

    def get_source_count(self):
        """
        Returns the number of sources considered (honoring discovery_only).
        """
        return len(self.get_sources())