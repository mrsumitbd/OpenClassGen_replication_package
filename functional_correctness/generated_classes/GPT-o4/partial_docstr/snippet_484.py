class Bucket:
    '''
    Represents a Bucket of storage on S3

    Parameters
    ----------
    name : string
        name of the bucket
    service : string or boto3 resource, optional (Default is None)
        name of a service resource, such as 's3', or a boto3 resource instance.
    '''

    def __init__(self, name, service=None):
        if service is None:
            self._resource = boto3.resource('s3')
        elif isinstance(service, str):
            self._resource = boto3.resource(service)
        else:
            self._resource = service
        self.name = name
        # client for list operations
        self._client = self._resource.meta.client

    def list(self, prefix='', delimiter=None):
        '''Limits a list of Bucket's objects based on prefix and delimiter.'''
        params = {'Bucket': self.name, 'Prefix': prefix}
        if delimiter is not None:
            params['Delimiter'] = delimiter
        paginator = self._client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(**params)

        results = []
        for page in page_iterator:
            for obj in page.get('Contents', []):
                results.append(obj['Key'])
        return results