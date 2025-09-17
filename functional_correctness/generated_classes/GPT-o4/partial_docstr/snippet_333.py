class ComponentResult(object):
    """The results of a single component"""

    def __init__(self, component_name, json_data, api_code, api_code_description):
        """
        Args:
            component_name (str): Name of the component.
            json_data (dict): JSON data returned from the API for this object.
            api_code (int): The HouseCanary business logic error code.
            api_code_description (str): The HouseCanary business logic error description.
        """
        self.component_name = component_name
        self.json_data = json_data
        self.api_code = api_code
        self.api_code_description = api_code_description

    def has_error(self):
        """Returns whether this component had a business logic error"""
        return self.api_code is not None and self.api_code != 0

    def get_error(self):
        """Gets the error of this component, if any"""
        if not self.has_error():
            return None
        return {
            'component': self.component_name,
            'code': self.api_code,
            'description': self.api_code_description
        }