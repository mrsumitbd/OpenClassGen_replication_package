class Assembly:
    def __init__(self, url):
        ''' Connect to an assembly that points to the assembly specified with the url.

        Args:
            - url (str): The url of the onshape item
        '''
        self.url = url
        self.session = requests.Session()

    def insert(self, part):
        ''' Insert a part into this assembly.

        Args:
            - part (onshapepy.part.Part) A Part instance that will be inserted.

        Returns:
            - requests.Response: Onshape response data

        '''
        # Assuming the part has a method to get its data for insertion
        part_data = part.get_data() if hasattr(part, 'get_data') else part
        
        # Make API call to insert the part into the assembly
        response = self.session.post(
            f"{self.url}/insert",
            json=part_data
        )
        
        return response