class AstromData(object):
    '''
    Encapsulates data extracted from an .astrom file.
    '''

    def __init__(self, observations, sys_header, sources, discovery_only=False):
        '''
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
        '''
        self.observations = observations
        self.sys_header = sys_header
        self.sources = sources
        self.discovery_only = discovery_only

    def get_reading_count(self):
        if not self.observations:
            return 0
        return len(self.observations)

    def get_sources(self):
        return self.sources

    def get_source_count(self):
        if not self.sources:
            return 0
        return len(self.sources)