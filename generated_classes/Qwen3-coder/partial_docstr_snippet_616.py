class BlacklistEntry(object):
    '''
    Args:
        plugin_type(str): Parent type
        name(str): Plugin name
        version(str): Plugin version
        operator(str): Comparison operator ('=', '==', '!=', '<', '<=', '>', '>=')

    **Container for blacklist entry**

    If ``operator`` is :py:data:`None` or not specified, it defaults to '=='.

    One of ``plugin_type``, ``name``, or ``version`` must be specified.
    If any are unspecified or :py:data:`None`, they are treated as a wildcard.

    In order to be more compatible with parsed text,
    the order of ``operator`` and ``version`` can be swapped. The following are equivalent:

    .. code-block:: python

        BlacklistEntry('parser', 'json', '1.0', '>=')

    .. code-block:: python

            BlacklistEntry('parser', 'json', '>=', '1.0')

    ``version`` is evaluated using :py:func:`pkg_resources.parse_version`
    and should conform to `PEP 440`_

    .. _PEP 440: https://www.python.org/dev/peps/pep-0440/
    '''

    def __init__(self, plugin_type=None, name=None, version=None, operator=None):
        # Check that at least one of plugin_type, name, or version is specified
        if plugin_type is None and name is None and version is None:
            raise ValueError("One of plugin_type, name, or version must be specified")
        
        # Handle swapped version and operator
        valid_operators = {'=', '==', '!=', '<', '<=', '>', '>='}
        if version in valid_operators and operator not in valid_operators:
            # version contains operator, operator contains version
            version, operator = operator, version
        
        # Set default operator if None or not specified
        if operator is None:
            operator = '=='
        
        # Validate operator
        if operator not in valid_operators:
            raise ValueError(f"Invalid operator: {operator}")
        
        self.plugin_type = plugin_type
        self.name = name
        self.version = version
        self.operator = operator
        
        # Parse version if it's specified
        if self.version is not None:
            self.parsed_version = pkg_resources.parse_version(self.version)
        else:
            self.parsed_version = None

    def __repr__(self):
        return f"BlacklistEntry(plugin_type={self.plugin_type!r}, name={self.name!r}, version={self.version!r}, operator={self.operator!r})"