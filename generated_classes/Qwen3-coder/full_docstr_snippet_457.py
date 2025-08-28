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
        
        for cls in clslist:
            if hasattr(cls, 'initMap') and cls.initMap is not None:
                self._extract_fields(cls.initMap)
    
    def _extract_fields(self, init_map):
        """Recursively extract required and optional fields from initMap."""
        if isinstance(init_map, dict):
            for key, value in init_map.items():
                if isinstance(value, dict):
                    # Check if this is a field specification
                    if 'required' in value:
                        if value['required']:
                            self.required_fields.add(key)
                        else:
                            self.optional_fields.add(key)
                    # Recursively process nested maps
                    self._extract_fields(value)
                elif key == 'required' and isinstance(value, bool):
                    # This is a required flag, already handled above
                    pass
                else:
                    # Recursively process nested structures
                    self._extract_fields(value)
    
    def __call__(self, systemConfig):
        '''
        Args:
            systemConfig (dict): A systemConfig dictionary to filter

        Returns:
            dict: Filtered dictionary

        Raises:
            ValueError: If a required key is not in the systemConfig
        '''
        # Check if all required fields are present
        missing_required = self.required_fields - systemConfig.keys()
        if missing_required:
            raise ValueError(f"Required keys missing from systemConfig: {missing_required}")
        
        # Filter the dictionary to only include valid fields
        valid_fields = self.required_fields | self.optional_fields
        filtered_config = {key: value for key, value in systemConfig.items() 
                          if key in valid_fields}
        
        return filtered_config