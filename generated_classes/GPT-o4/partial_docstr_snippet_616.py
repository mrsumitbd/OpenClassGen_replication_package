class BlacklistEntry(object):
    '''
    Args:
        plugin_type(str): Parent type
        name(str): Plugin name
        version(str): Plugin version
        operator(str): Comparison operator ('=', '==', '!=', '<', '<=', '>', '>=')

    **Container for blacklist entry**
    '''
    _VALID_OPERATORS = {'=', '==', '!=', '<', '<=', '>', '>='}

    def __init__(self, plugin_type=None, name=None, version=None, operator=None):
        # allow swapping operator and version
        if version in self._VALID_OPERATORS and (operator is None or operator not in self._VALID_OPERATORS):
            version, operator = operator, version

        if operator is None:
            operator = '=='
        if operator not in self._VALID_OPERATORS:
            raise ValueError("Invalid operator: %r" % operator)

        if plugin_type is None and name is None and version is None:
            raise ValueError("At least one of plugin_type, name, or version must be specified")

        self.plugin_type = plugin_type
        self.name = name
        self.operator = operator
        self.version = parse_version(version) if version is not None else None

    def __repr__(self):
        return (
            "BlacklistEntry(plugin_type=%r, name=%r, "
            "operator=%r, version=%r)"
            % (self.plugin_type, self.name, self.operator, self.version)
        )