class ModelMonitoringFile(object):
    '''Represents a file with a body and an S3 uri.'''

    def __init__(self, body_dict, file_s3_uri, kms_key, sagemaker_session):
        '''Initializes a file with a body and an S3 uri.

        Args:
            body_dict (str): The body of the JSON file.
            file_s3_uri (str): The uri of the JSON file.
            kms_key (str): The kms key to be used to decrypt the file in S3.
            sagemaker_session (sagemaker.session.Session): A SageMaker Session
                object, used for SageMaker interactions (default: None). If not
                specified, one is created using the default AWS configuration
                chain.

        '''
        self.body_dict = body_dict
        self.file_s3_uri = file_s3_uri
        self.kms_key = kms_key
        self.sagemaker_session = sagemaker_session or Session()

    def save(self, new_save_location_s3_uri=None):
        '''Save the current instance's body to s3 using the instance's s3 path.

        The S3 path can be overridden by providing one. This also overrides the
        default save location for this object.

        Args:
            new_save_location_s3_uri (str): Optional. The S3 path to save the file to. If not
                provided, the file is saved in place in S3. If provided, the file's S3 path is
                permanently updated.

        Returns:
            str: The s3 location to which the file was saved.

        '''
        if new_save_location_s3_uri:
            self.file_s3_uri = new_save_location_s3_uri
        
        # Convert body_dict to JSON string
        body_json = json.dumps(self.body_dict)
        
        # Upload to S3
        self.sagemaker_session.upload_data(
            path=body_json,
            key_prefix=self._get_key_prefix(),
            bucket=self._get_bucket(),
            kms_key=self.kms_key
        )
        
        return self.file_s3_uri
    
    def _get_bucket(self):
        '''Extract bucket name from S3 URI'''
        return self.file_s3_uri.split('/')[2]
    
    def _get_key_prefix(self):
        '''Extract key prefix from S3 URI'''
        return '/'.join(self.file_s3_uri.split('/')[3:])