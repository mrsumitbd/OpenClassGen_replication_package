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
        # type: (...) -> None
        self._credential = credential
        self._subscription_id = subscription_id
        self._base_url = base_url
        
        if base_url is None:
            self._base_url = "https://management.azure.com"
        
        # Initialize all operation clients
        from azure.mgmt.applicationinsights.v2015_05_01.operations import Operations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import AnnotationsOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import APIKeysOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import ExportConfigurationsOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import ComponentCurrentBillingFeaturesOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import ComponentQuotaStatusOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import ComponentFeatureCapabilitiesOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import ComponentAvailableFeaturesOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import ProactiveDetectionConfigurationsOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import ComponentsOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import WorkItemConfigurationsOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import FavoritesOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import WebTestLocationsOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import WebTestsOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import AnalyticsItemsOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import WorkbooksOperations
        from azure.mgmt.applicationinsights.v2015_05_01.operations import MyWorkbooksOperations
        
        self.operations = Operations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.annotations = AnnotationsOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.api_keys = APIKeysOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.export_configurations = ExportConfigurationsOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.component_current_billing_features = ComponentCurrentBillingFeaturesOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.component_quota_status = ComponentQuotaStatusOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.component_feature_capabilities = ComponentFeatureCapabilitiesOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.component_available_features = ComponentAvailableFeaturesOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.proactive_detection_configurations = ProactiveDetectionConfigurationsOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.components = ComponentsOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.work_item_configurations = WorkItemConfigurationsOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.favorites = FavoritesOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.web_test_locations = WebTestLocationsOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.web_tests = WebTestsOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.analytics_items = AnalyticsItemsOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.workbooks = WorkbooksOperations(self._credential, self._subscription_id, self._base_url, **kwargs)
        self.my_workbooks = MyWorkbooksOperations(self._credential, self._subscription_id, self._base_url, **kwargs)

    def close(self):
        # type: () -> None
        # Close all operation clients
        self.operations.close()
        self.annotations.close()
        self.api_keys.close()
        self.export_configurations.close()
        self.component_current_billing_features.close()
        self.component_quota_status.close()
        self.component_feature_capabilities.close()
        self.component_available_features.close()
        self.proactive_detection_configurations.close()
        self.components.close()
        self.work_item_configurations.close()
        self.favorites.close()
        self.web_test_locations.close()
        self.web_tests.close()
        self.analytics_items.close()
        self.workbooks.close()
        self.my_workbooks.close()

    def __enter__(self):
        # type: () -> ApplicationInsightsManagementClient
        return self

    def __exit__(self, *exc_details):
        # type: (*Any) -> None
        self.close()