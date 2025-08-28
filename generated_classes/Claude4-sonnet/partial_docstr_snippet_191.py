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
        self.definition_format_properties = json_resource_tag.get('definitionFormatProperties', False)
        self.description = json_resource_tag.get('description', '')
        self.name = json_resource_tag.get('name', '')
        self.properties_definition = json_resource_tag.get('propertiesDefinition', [])
        self.reserved = json_resource_tag.get('reserved', False)

    def __str__(self):
        return f"ResourceTag(name='{self.name}', description='{self.description}', reserved={self.reserved}, definition_format_properties={self.definition_format_properties})"