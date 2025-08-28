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
        if not base_url:
            base_url = 'https://management.azure.com'
        self._config = ApplicationInsightsManagementClientConfiguration(credential, subscription_id, **kwargs)
        self._client = ARMPipelineClient(base_url=base_url, config=self._config, **kwargs)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        from azure.mgmt.applicationinsights.v2020_02_02_preview.operations import ComponentsOperations
        self.components = ComponentsOperations(
            self._client, self._config, self._serialize, self._deserialize)

    def close(self):
        self._client.close()

    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, *exc_details):
        self._client.__exit__(*exc_details)