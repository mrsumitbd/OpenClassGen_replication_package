class CounterpartMapping:
    '''This class carries the pieces needed to perform mappings.

    Sections represent groups that enable this mapping to apply
    different rules depending on attributes of the input.  The two
    sections here are COUNTERPART_MAP and COUNTERPART_DIR.

    CounterpartMapping is much like a collections.Mapping, but it does
    not support the __iter__ and __len__ methods specified for that
    class.  Unlike mapping functions with a fixed set of keys, the
    domain may be unknown when the COUNTERPART_DIR section is present
    in the config.
    '''

    def __init__(self, map_config):
        self._map = {}
        self._prepend = None
        if map_config is None:
            return
        cm = map_config.get('COUNTERPART_MAP')
        if cm:
            self._map.update(cm)
        cd = map_config.get('COUNTERPART_DIR')
        if cd:
            self._prepend = cd.get('prepend_path')

    def __getitem__(self, known):
        '''If the counterpart is named explicitly in COUNTERPART_MAP, return
        it.  When `prepend_path` is given in the COUNTERPART_DIR
        section, it is prepended to all input that lacks an explicitly
        named counterpart in COUNTERPART_MAP.
        '''
        if known in self._map:
            return self._map[known]
        if self._prepend is not None:
            return os.path.join(self._prepend, known)
        raise KeyError(known)