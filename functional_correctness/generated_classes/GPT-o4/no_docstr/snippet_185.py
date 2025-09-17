class CollectionRunner:

    def __init__(self, policies, options, reporter):
        self.policies = policies
        self.options = options
        self.reporter = reporter

    def run(self) -> bool:
        success = True
        provider = self.get_provider()
        event = self.get_event()
        for policy in self.policies:
            if not self.match_type(getattr(self.options, 'resource_type', None), policy):
                continue
            graph = None
            if hasattr(policy, 'get_graph'):
                graph = policy.get_graph(provider, event)
            resources = []
            if hasattr(policy, 'get_resources'):
                resources = policy.get_resources(provider, event)
            result = self.run_policy(policy, graph, resources, event, getattr(policy, 'resource_type', None))
            success = success and result
        return success

    def run_policy(self, policy, graph, resources, event, resource_type):
        try:
            if hasattr(self.reporter, 'on_start'):
                self.reporter.on_start(policy, event, resource_type)
            result = policy.run(graph, resources, event)
            if hasattr(self.reporter, 'on_complete'):
                self.reporter.on_complete(policy, result)
            return bool(result)
        except Exception as e:
            if hasattr(self.reporter, 'on_error'):
                self.reporter.on_error(policy, e)
            return False

    def get_provider(self):
        return getattr(self.options, 'provider', None)

    def get_event(self):
        return getattr(self.options, 'event', None)

    @staticmethod
    def match_type(rtype, p):
        if not rtype:
            return True
        rt = getattr(p, 'resource_type', None)
        if isinstance(rtype, str):
            return rt == rtype
        try:
            return any(rt == r for r in rtype)
        except TypeError:
            return False