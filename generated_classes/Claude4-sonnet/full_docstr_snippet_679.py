class Resolver:
    '''
    An I{abstract} schema-type resolver.
    @ivar schema: A schema object.
    @type schema: L{xsd.schema.Schema}
    '''

    def __init__(self, schema):
        '''
        @param schema: A schema object.
        @type schema: L{xsd.schema.Schema}
        '''
        self.schema = schema

    def find(self, name, resolved=True):
        '''
        Get the definition object for the schema object by name.
        @param name: The name of a schema object.
        @type name: basestring
        @param resolved: A flag indicating that the fully resolved type
            should be returned.
        @type resolved: boolean
        @return: The found schema I{type}
        @rtype: L{xsd.sxbase.SchemaObject}
        '''
        raise NotImplementedError("Subclasses must implement find method")