class CollectionRunner:
    def __init__(self, policies, options, reporter):
        self.policies = policies
        self.options = options
        self.reporter = reporter
        self.provider = None
        self.event = None

    def run(self) -> bool:
        try:
            self.provider = self.get_provider()
            self.event = self.get_event()
            
            for policy in self.policies:
                resource_type = policy.get_resource_type()
                resources = self.provider.get_resources(resource_type)
                graph = self.provider.get_resource_graph(resource_type)
                
                self.run_policy(policy, graph, resources, self.event, resource_type)
            
            return True
        except Exception as e:
            if self.reporter:
                self.reporter.report_error(e)
            return False

    def run_policy(self, policy, graph, resources, event, resource_type):
        if self.match_type(resource_type, policy):
            policy.evaluate(resources, graph, event)
            if self.reporter:
                self.reporter.report_policy_result(policy, resources)

    def get_provider(self):
        # Assuming there's a provider factory or registry
        from .provider import ProviderFactory
        return ProviderFactory.get_provider(self.options)

    def get_event(self):
        # Assuming there's an event factory or context
        from .event import EventFactory
        return EventFactory.create_event(self.options)

    @staticmethod
    def match_type(rtype, p):
        policy_type = p.get_resource_type()
        return rtype == policy_type or policy_type == '*' or rtype in policy_type