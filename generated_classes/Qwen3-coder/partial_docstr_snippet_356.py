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
        self.map_config = map_config
        self.counterpart_map = map_config.get('COUNTERPART_MAP', {})
        self.counterpart_dir = map_config.get('COUNTERPART_DIR', {})

    def __getitem__(self, known):
        '''If the counterpart is named explicitly in COUNTERPART_MAP, return
        it.  When `prepend_path` is given in the COUNTERPART_DIR
        section, it is prepended to all input that lacks an explicitly
        named counterpart in COUNTERPART_MAP.

        '''
        if known in self.counterpart_map:
            return self.counterpart_map[known]
        
        prepend_path = self.counterpart_dir.get('prepend_path')
        if prepend_path is not None:
            return prepend_path + known
        
        raise KeyError(known)