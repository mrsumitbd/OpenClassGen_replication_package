class CompleterDescriber(object):
    '''Describes how to autocomplete a resource.

    You give this class a service/operation/param and it will
    describe to you how you can autocomplete values for the
    provided parameter.

    It's up to the caller to actually take that description
    and make the appropriate service calls + filtering to
    extract out the server side values.

    '''

    def __init__(self, resource_index):
        self._resource_index = resource_index

    def describe_autocomplete(self, service, operation, param):
        '''Describe operation and args needed for server side completion.

        :type service: str
        :param service: The AWS service name.

        :type operation: str
        :param operation: The AWS operation name.

        :type param: str
        :param param: The name of the parameter being completed.  This must
            match the casing in the service model (e.g. InstanceIds, not
            --instance-ids).

        :rtype: ServerCompletion
        :return: A ServerCompletion object that describes what API call to make
            in order to complete the response.

        '''
        try:
            ops = self._resource_index[service][operation]
        except (KeyError, TypeError):
            return None
        completion = ops.get(param)
        if not completion:
            return None
        # support single dict or list of dicts
        comp = completion[0] if isinstance(completion, list) and completion else completion
        args = comp.get('parameters', comp.get('params', {})) or {}
        path = comp.get('path')
        svc = comp.get('service', service)
        op = comp.get('operation', operation)
        return ServerCompletion(svc, op, args, path)