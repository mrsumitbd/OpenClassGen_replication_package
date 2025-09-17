class Bucket:
    '''
    Represents a Bucket of storage on S3

    Parameters
    ----------
    name : string
        name of the bucket
    service : string, optional (Default is None)
        name of a service resource, such as SQS, EC2, etc.

    '''

    def __init__(self, name, service=None):
        self.name = name
        self.service = service
        self.objects = []

    def list(self, prefix='', delimiter=None):
        '''Limits a list of Bucket's objects based on prefix and delimiter.'''
        filtered_objects = []
        
        for obj in self.objects:
            # Check if object name starts with the prefix
            if obj.startswith(prefix):
                # If delimiter is specified, check for delimiter behavior
                if delimiter:
                    # Find the first occurrence of delimiter after the prefix
                    prefix_end = len(prefix)
                    delimiter_pos = obj.find(delimiter, prefix_end)
                    
                    # If delimiter found, include the prefix + up to and including delimiter
                    # Otherwise, include the whole object name if it matches prefix
                    if delimiter_pos != -1:
                        filtered_objects.append(obj[:delimiter_pos + 1])
                    else:
                        filtered_objects.append(obj)
                else:
                    # No delimiter, just check prefix
                    filtered_objects.append(obj)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_objects = []
        for obj in filtered_objects:
            if obj not in seen:
                seen.add(obj)
                unique_objects.append(obj)
        
        return unique_objects