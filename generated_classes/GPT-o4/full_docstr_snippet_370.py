class ExplainabilityAnalysisConfig:
    '''Analysis configuration for ModelExplainabilityMonitor.'''

    def __init__(self, explainability_config, model_config, headers=None, label_headers=None):
        '''Creates an analysis config dictionary.

        Args:
            explainability_config (sagemaker.clarify.ExplainabilityConfig): Config object related
                to explainability configurations.
            model_config (sagemaker.clarify.ModelConfig): Config object related to bias
                configurations.
            headers (list[str]): A list of feature names (without label) of model/endpoint input.
            label_headers (list[str]): List of headers, each for a predicted score in model output.
                It is used to beautify the analysis report by replacing placeholders like "label0".
        '''
        self.explainability_config = explainability_config
        self.model_config = model_config
        self.headers = headers
        self.label_headers = label_headers

    def _to_dict(self):
        '''Generates a request dictionary using the parameters provided to the class.'''
        config = {
            'ExplainabilityConfig': self.explainability_config.to_dict(),
            'ModelConfig': self.model_config.to_dict()
        }
        if self.headers is not None:
            config['Headers'] = self.headers
        if self.label_headers is not None:
            config['LabelHeaders'] = self.label_headers
        return config