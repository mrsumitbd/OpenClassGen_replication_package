class Versions(object):
    '''
    Version API client. It indicates the range of API versions supported by the appliance.

    '''

    def __init__(self, con):
        self._connection = con

    def get_version(self):
        '''
        Returns the range of possible API versions supported by the appliance.
        The response contains the current version and the minimum version.
        The current version is the recommended version to specify in the REST header.
        The other versions are supported for backward compatibility, but might not support the most current features.

        Returns:
            dict: The minimum and maximum supported API versions.
        '''
        response = self._connection.get('/api/versions')
        return response