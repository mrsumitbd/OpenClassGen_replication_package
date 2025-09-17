class ResourceTag(object):
    '''Resource tag defined in a Streams domain

    Attributes:
        definition_format_properties(bool): Indicates whether the resource definition consists of one or more
            properties.
        description(str): Tag description.
        name(str): Tag name.
        properties_definition(list(str)): Contains the properties of the resource definition. Only present if
            `definition_format_properties` is *True*.
        reserved(bool): If *True*, this tag is defined by IBM Streams, and cannot be modified.
    '''

    def __init__(self, json_resource_tag):
        required = ['definitionFormatProperties', 'description', 'name', 'reserved']
        for key in required:
            if key not in json_resource_tag:
                raise KeyError(f"Missing required field '{key}' in json_resource_tag")
        self.definition_format_properties = bool(json_resource_tag['definitionFormatProperties'])
        self.description = str(json_resource_tag['description'])
        self.name = str(json_resource_tag['name'])
        self.reserved = bool(json_resource_tag['reserved'])
        if self.definition_format_properties:
            props = json_resource_tag.get('propertiesDefinition', [])
            if not isinstance(props, list):
                raise TypeError("'propertiesDefinition' must be a list")
            self.properties_definition = [str(p) for p in props]

    def __str__(self):
        parts = [
            f"name='{self.name}'",
            f"description='{self.description}'",
            f"reserved={self.reserved}",
            f"definition_format_properties={self.definition_format_properties}"
        ]
        if getattr(self, 'properties_definition', None) is not None:
            parts.append(f"properties_definition={self.properties_definition}")
        return "ResourceTag(" + ", ".join(parts) + ")"