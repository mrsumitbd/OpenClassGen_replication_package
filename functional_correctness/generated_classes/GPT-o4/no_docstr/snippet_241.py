class AmazonTransport(object):
    def __init__(self, config):
        """
        config: {
            "service": "sqs" or "sns",
            "region_name": "...",
            "aws_access_key_id": "...",
            "aws_secret_access_key": "...",
            "aws_session_token": "...",  # optional
            "queue_url": "...",          # for sqs
            "topic_arn": "..."           # for sns
        }
        """
        self.config = config
        self.client = None
        self.service = config.get("service", "sqs").lower()
        if self.service not in ("sqs", "sns"):
            raise ValueError("Unsupported service: %s" % self.service)

    def startup(self):
        params = {
            "region_name": self.config.get("region_name"),
            "aws_access_key_id": self.config.get("aws_access_key_id"),
            "aws_secret_access_key": self.config.get("aws_secret_access_key"),
        }
        token = self.config.get("aws_session_token")
        if token:
            params["aws_session_token"] = token
        if self.service == "sqs":
            self.client = boto3.client("sqs", **params)
            if not self.config.get("queue_url"):
                raise ValueError("queue_url is required for SQS")
        else:
            self.client = boto3.client("sns", **params)
            if not self.config.get("topic_arn"):
                raise ValueError("topic_arn is required for SNS")

    def deliver(self, message):
        if not self.client:
            raise RuntimeError("Client not initialized. Call startup() first.")
        try:
            if self.service == "sqs":
                resp = self.client.send_message(
                    QueueUrl=self.config["queue_url"],
                    MessageBody=message
                )
            else:
                resp = self.client.publish(
                    TopicArn=self.config["topic_arn"],
                    Message=message
                )
            return resp
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError("Failed to deliver message: %s" % e)

    def shutdown(self):
        # boto3 clients do not require explicit shutdown
        self.client = None