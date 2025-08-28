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
        if not isinstance(name, basestring):
            raise TypeError("Schema object name must be a string")
        obj = None
        for attr in ('types', 'elements', 'attributes',
                     'groups', 'attribute_groups', 'model_groups'):
            mapping = getattr(self.schema, attr, None)
            if mapping and name in mapping:
                obj = mapping[name]
                break
        if obj is None:
            raise KeyError("No such schema object: %r" % (name,))
        if not resolved:
            return obj
        visited = set()
        while True:
            key = (id(obj), getattr(obj, 'name', None))
            if key in visited:
                break
            visited.add(key)
            new_obj = None
            if hasattr(obj, 'type') and isinstance(obj.type, basestring):
                new_obj = self.find(obj.type)
            elif hasattr(obj, 'restriction') and obj.restriction is not None:
                base = getattr(obj.restriction, 'base', None)
                if isinstance(base, basestring):
                    new_obj = self.find(base)
            elif hasattr(obj, 'list') and obj.list is not None:
                it = getattr(obj.list, 'itemType', None)
                if isinstance(it, basestring):
                    new_obj = self.find(it)
            elif hasattr(obj, 'content') and obj.content is not None:
                content = obj.content
                ext = getattr(content, 'extension', None)
                if ext is not None and isinstance(getattr(ext, 'base', None), basestring):
                    new_obj = self.find(ext.base)
                else:
                    restr = getattr(content, 'restriction', None)
                    if restr is not None and isinstance(getattr(restr, 'base', None), basestring):
                        new_obj = self.find(restr.base)
            if new_obj is None:
                break
            obj = new_obj
        return obj