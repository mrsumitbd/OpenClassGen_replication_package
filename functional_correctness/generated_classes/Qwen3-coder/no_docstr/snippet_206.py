class PopulateResponseMixin:
    @classmethod
    def from_response(cls, raw_response):
        """
        Create an instance of the class from a raw response dictionary.
        
        Args:
            raw_response (dict): The raw response data to populate the object with
            
        Returns:
            An instance of the class populated with the response data
        """
        instance = cls()
        
        # Get all attributes that can be set on the instance
        for key, value in raw_response.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
            elif hasattr(instance, f"_{key}"):
                # Try setting private attribute if public doesn't exist
                setattr(instance, f"_{key}", value)
        
        return instance