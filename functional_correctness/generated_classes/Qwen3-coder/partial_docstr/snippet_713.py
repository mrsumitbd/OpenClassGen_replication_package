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
        self.resource_index = resource_index

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
        # Look up the completion information in the resource index
        service_completions = self.resource_index.get(service, {})
        operation_completions = service_completions.get(operation, {})
        param_completion = operation_completions.get(param)
        
        if param_completion is None:
            return None
            
        # Extract the service, operation, and args from the completion info
        completion_service = param_completion.get('service', service)
        completion_operation = param_completion.get('operation', operation)
        completion_args = param_completion.get('args', {})
        
        return ServerCompletion(completion_service, completion_operation, completion_args)