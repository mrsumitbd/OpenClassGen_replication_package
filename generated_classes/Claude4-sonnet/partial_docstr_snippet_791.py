class ApplicationInsightsManagementClient(object):
    '''Composite Swagger for Application Insights Management Client.

    :ivar operations: Operations operations
    :vartype operations: azure.mgmt.applicationinsights.v2015_05_01.operations.Operations
    :ivar annotations: AnnotationsOperations operations
    :vartype annotations: azure.mgmt.applicationinsights.v2015_05_01.operations.AnnotationsOperations
    :ivar api_keys: APIKeysOperations operations
    :vartype api_keys: azure.mgmt.applicationinsights.v2015_05_01.operations.APIKeysOperations
    :ivar export_configurations: ExportConfigurationsOperations operations
    :vartype export_configurations: azure.mgmt.applicationinsights.v2015_05_01.operations.ExportConfigurationsOperations
    :ivar component_current_billing_features: ComponentCurrentBillingFeaturesOperations operations
    :vartype component_current_billing_features: azure.mgmt.applicationinsights.v2015_05_01.operations.ComponentCurrentBillingFeaturesOperations
    :ivar component_quota_status: ComponentQuotaStatusOperations operations
    :vartype component_quota_status: azure.mgmt.applicationinsights.v2015_05_01.operations.ComponentQuotaStatusOperations
    :ivar component_feature_capabilities: ComponentFeatureCapabilitiesOperations operations
    :vartype component_feature_capabilities: azure.mgmt.applicationinsights.v2015_05_01.operations.ComponentFeatureCapabilitiesOperations
    :ivar component_available_features: ComponentAvailableFeaturesOperations operations
    :vartype component_available_features: azure.mgmt.applicationinsights.v2015_05_01.operations.ComponentAvailableFeaturesOperations
    :ivar proactive_detection_configurations: ProactiveDetectionConfigurationsOperations operations
    :vartype proactive_detection_configurations: azure.mgmt.applicationinsights.v2015_05_01.operations.ProactiveDetectionConfigurationsOperations
    :ivar components: ComponentsOperations operations
    :vartype components: azure.mgmt.applicationinsights.v2015_05_01.operations.ComponentsOperations
    :ivar work_item_configurations: WorkItemConfigurationsOperations operations
    :vartype work_item_configurations: azure.mgmt.applicationinsights.v2015_05_01.operations.WorkItemConfigurationsOperations
    :ivar favorites: FavoritesOperations operations
    :vartype favorites: azure.mgmt.applicationinsights.v2015_05_01.operations.FavoritesOperations
    :ivar web_test_locations: WebTestLocationsOperations operations
    :vartype web_test_locations: azure.mgmt.applicationinsights.v2015_05_01.operations.WebTestLocationsOperations
    :ivar web_tests: WebTestsOperations operations
    :vartype web_tests: azure.mgmt.applicationinsights.v2015_05_01.operations.WebTestsOperations
    :ivar analytics_items: AnalyticsItemsOperations operations
    :vartype analytics_items: azure.mgmt.applicationinsights.v2015_05_01.operations.AnalyticsItemsOperations
    :ivar workbooks: WorkbooksOperations operations
    :vartype workbooks: azure.mgmt.applicationinsights.v2015_05_01.operations.WorkbooksOperations
    :ivar my_workbooks: MyWorkbooksOperations operations
    :vartype my_workbooks: azure.mgmt.applicationinsights.v2015_05_01.operations.MyWorkbooksOperations
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
        
        client_models = {k: v for k, v in kwargs.items() if k.endswith('_models')}
        self._serialize = kwargs.get('serializer')
        self._deserialize = kwargs.get('deserializer')
        
        self.operations = Operations(self._client, self._config, self._serialize, self._deserialize)
        self.annotations = AnnotationsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.api_keys = APIKeysOperations(self._client, self._config, self._serialize, self._deserialize)
        self.export_configurations = ExportConfigurationsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.component_current_billing_features = ComponentCurrentBillingFeaturesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.component_quota_status = ComponentQuotaStatusOperations(self._client, self._config, self._serialize, self._deserialize)
        self.component_feature_capabilities = ComponentFeatureCapabilitiesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.component_available_features = ComponentAvailableFeaturesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.proactive_detection_configurations = ProactiveDetectionConfigurationsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.components = ComponentsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.work_item_configurations = WorkItemConfigurationsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.favorites = FavoritesOperations(self._client, self._config, self._serialize, self._deserialize)
        self.web_test_locations = WebTestLocationsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.web_tests = WebTestsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.analytics_items = AnalyticsItemsOperations(self._client, self._config, self._serialize, self._deserialize)
        self.workbooks = WorkbooksOperations(self._client, self._config, self._serialize, self._deserialize)
        self.my_workbooks = MyWorkbooksOperations(self._client, self._config, self._serialize, self._deserialize)

    def close(self):
        self._client.close()

    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, *exc_details):
        self._client.__exit__(*exc_details)