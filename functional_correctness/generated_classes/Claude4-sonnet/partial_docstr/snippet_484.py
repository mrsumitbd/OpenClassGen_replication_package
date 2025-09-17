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

    def list(self, prefix='', delimiter=None):
        '''Limits a list of Bucket's objects based on prefix and delimiter.'''
        import boto3
        
        s3_client = boto3.client('s3')
        
        kwargs = {
            'Bucket': self.name,
            'Prefix': prefix
        }
        
        if delimiter is not None:
            kwargs['Delimiter'] = delimiter
        
        objects = []
        paginator = s3_client.get_paginator('list_objects_v2')
        
        for page in paginator.paginate(**kwargs):
            if 'Contents' in page:
                objects.extend(page['Contents'])
        
        return objects