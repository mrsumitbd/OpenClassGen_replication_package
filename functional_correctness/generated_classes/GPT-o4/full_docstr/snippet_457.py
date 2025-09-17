class SCFilter(object):
    '''
    A SCFilter class is initialized with a list of classes as arguments.
    For any of those classes that are AttributeMapper subclasses, SCFilter
    determines the required fields in their initMap trees, and the optional
    fields. When called, the SCFilter discards any key in the passed dictionary
    that does not match one of those fields, and raises an error if any of the
    required fields are not present.
    '''
    def __init__(self, clslist):
        self._required = set()
        self._optional = set()
        # gather fields from all AttributeMapper subclasses
        for cls in clslist:
            try:
                if issubclass(cls, AttributeMapper):
                    init_map = getattr(cls, 'initMap', {})
                    self._parse_map(init_map)
            except Exception:
                continue
        self._all = self._required.union(self._optional)

    def _parse_map(self, mp):
        """
        Recursively parse an initMap tree assumed to be a dict
        mapping field names to dicts with optional 'required' bool
        and optional nested dicts.
        """
        if not isinstance(mp, dict):
            return
        for key, val in mp.items():
            if isinstance(val, dict):
                req = val.get('required', False)
                if req:
                    self._required.add(key)
                else:
                    self._optional.add(key)
                # if there is a nested map under 'fields' or 'children', recurse
                for child_key in ('fields', 'children', 'map'):
                    if child_key in val:
                        self._parse_map(val[child_key])
            else:
                # leaf without explicit required flag → optional
                self._optional.add(key)

    def __call__(self, systemConfig):
        missing = self._required - set(systemConfig.keys())
        if missing:
            raise ValueError(f"Missing required fields: {sorted(missing)}")
        # keep only allowed keys
        return {k: v for k, v in systemConfig.items() if k in self._all}