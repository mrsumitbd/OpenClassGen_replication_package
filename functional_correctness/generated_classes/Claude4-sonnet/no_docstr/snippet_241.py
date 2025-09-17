class AmazonTransport(object):

    def __init__(self, config):
        self.config = config
        self.client = None
        self.queue_url = config.get('queue_url')
        self.topic_arn = config.get('topic_arn')
        self.region = config.get('region', 'us-east-1')
        self.service = config.get('service', 'sqs')  # 'sqs' or 'sns'
        self.aws_access_key_id = config.get('aws_access_key_id')
        self.aws_secret_access_key = config.get('aws_secret_access_key')

    def startup(self):
        try:
            if self.service == 'sqs':
                self.client = boto3.client(
                    'sqs',
                    region_name=self.region,
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key
                )
            elif self.service == 'sns':
                self.client = boto3.client(
                    'sns',
                    region_name=self.region,
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key
                )
        except (NoCredentialsError, ClientError) as e:
            raise Exception(f"Failed to initialize AWS client: {str(e)}")

    def deliver(self, message):
        if not self.client:
            raise Exception("Transport not started. Call startup() first.")
        
        try:
            if isinstance(message, dict):
                message_body = json.dumps(message)
            else:
                message_body = str(message)
            
            if self.service == 'sqs':
                response = self.client.send_message(
                    QueueUrl=self.queue_url,
                    MessageBody=message_body
                )
                return response.get('MessageId')
            elif self.service == 'sns':
                response = self.client.publish(
                    TopicArn=self.topic_arn,
                    Message=message_body
                )
                return response.get('MessageId')
        except ClientError as e:
            raise Exception(f"Failed to deliver message: {str(e)}")

    def shutdown(self):
        if self.client:
            self.client = None