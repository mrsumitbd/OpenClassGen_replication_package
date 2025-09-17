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
        from azure.mgmt.applicationinsights.v2020_02_02_preview.operations import ComponentsOperations
        from azure.core.pipeline import Pipeline
        from azure.core.pipeline.transport import RequestsTransport
        from azure.core.pipeline.policies import (
            BearerTokenCredentialPolicy,
            ContentDecodePolicy,
            DistributedTracingPolicy,
            HttpLoggingPolicy,
            RequestIdPolicy,
            RetryPolicy,
            UserAgentPolicy,
        )
        from azure.mgmt.core.policies import ARMChallengeAuthenticationPolicy, ARMHttpLoggingPolicy

        self._config = kwargs.get('config') or self._create_default_config(credential, subscription_id, base_url, **kwargs)
        self._client = kwargs.get('client') or self._create_client(self._config, credential, **kwargs)
        
        self.components = ComponentsOperations(self._client, self._config)

    def _create_default_config(self, credential, subscription_id, base_url, **kwargs):
        from azure.mgmt.applicationinsights.v2020_02_02_preview._configuration import ApplicationInsightsManagementClientConfiguration
        return ApplicationInsightsManagementClientConfiguration(credential, subscription_id, base_url, **kwargs)

    def _create_client(self, config, credential, **kwargs):
        from azure.core.pipeline import Pipeline
        from azure.core.pipeline.transport import RequestsTransport
        from azure.core.pipeline.policies import (
            BearerTokenCredentialPolicy,
            ContentDecodePolicy,
            DistributedTracingPolicy,
            HttpLoggingPolicy,
            RequestIdPolicy,
            RetryPolicy,
            UserAgentPolicy,
        )
        from azure.mgmt.core.policies import ARMChallengeAuthenticationPolicy, ARMHttpLoggingPolicy

        policies = [
            RequestIdPolicy(**kwargs),
            UserAgentPolicy(**kwargs),
            RetryPolicy(**kwargs),
            BearerTokenCredentialPolicy(credential, config.credential_scopes, **kwargs),
            ContentDecodePolicy(**kwargs),
            DistributedTracingPolicy(**kwargs),
            HttpLoggingPolicy(**kwargs),
            ARMHttpLoggingPolicy(**kwargs),
        ]

        transport = kwargs.get('transport') or RequestsTransport(**kwargs)
        pipeline = Pipeline(transport, policies)

        from azure.core.rest import HttpRequest
        client = HttpRequest('GET', config.base_url)
        client._client = pipeline
        return client

    def close(self):
        if hasattr(self, '_client') and self._client:
            if hasattr(self._client, 'close'):
                self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.close()