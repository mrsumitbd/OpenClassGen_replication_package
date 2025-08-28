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
        '''
        SCFilter(clslist)

        Args:
            clslist (list): List of classes from which to build the filter

        Returns:
            new SCFilter instance
        '''
        self.required_fields = set()
        self.optional_fields = set()
        self.all_fields = set()
        
        for cls in clslist:
            if hasattr(cls, 'initMap') and hasattr(cls, '__bases__'):
                # Check if it's an AttributeMapper subclass
                is_attribute_mapper = False
                for base in cls.__mro__:
                    if base.__name__ == 'AttributeMapper':
                        is_attribute_mapper = True
                        break
                
                if is_attribute_mapper:
                    self._extract_fields_from_initmap(cls.initMap)
        
        self.all_fields = self.required_fields | self.optional_fields

    def _extract_fields_from_initmap(self, initmap):
        for key, value in initmap.items():
            if isinstance(value, dict):
                if value.get('required', False):
                    self.required_fields.add(key)
                else:
                    self.optional_fields.add(key)
                
                # Recursively process nested mappings
                if 'initMap' in value:
                    self._extract_fields_from_initmap(value['initMap'])
            else:
                # If value is not a dict, treat as optional field
                self.optional_fields.add(key)

    def __call__(self, systemConfig):
        '''
        Args:
            systemConfig (dict): A systemConfig dictionary to filter

        Returns:
            dict: Filtered dictionary

        Raises:
            ValueError: If a required key is not in the systemConfig
        '''
        # Check for missing required fields
        missing_required = self.required_fields - set(systemConfig.keys())
        if missing_required:
            raise ValueError(f"Required fields missing: {missing_required}")
        
        # Filter the dictionary to only include known fields
        filtered_config = {}
        for key, value in systemConfig.items():
            if key in self.all_fields:
                filtered_config[key] = value
        
        return filtered_config