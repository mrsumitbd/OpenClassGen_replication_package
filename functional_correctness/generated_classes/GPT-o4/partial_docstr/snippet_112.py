class ApplicationInsightsManagementClient(object):
    '''Composite Swagger for Application Insights Management Client.

    :ivar components: ComponentsOperations operations
    :vartype components: azure.mgmt.applicationinsights.v2020_02_02_preview.operations.ComponentsOperations
    :param credential: Credential needed for the client to connect to Azure.
    :type credential: ~azure.core.credentials.TokenCredential
    :param subscription_id: The ID of the target subscription.
    :type subscription_id: str
    :param str base_url: Service URL
    '''

    def __init__(
        self,
        credential,  # type: "TokenCredential"
        subscription_id,  # type: str
        base_url=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        self.credential = credential
        self.subscription_id = subscription_id
        self.base_url = base_url or "https://management.azure.com"
        self.components = ComponentsOperations(
            credential=self.credential,
            subscription_id=self.subscription_id,
            base_url=self.base_url,
            **kwargs
        )

    def close(self):
        # nothing to close for this client
        return

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.close()