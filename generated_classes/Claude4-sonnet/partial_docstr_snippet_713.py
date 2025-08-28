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
        if service not in self._resource_index:
            return None
        
        service_data = self._resource_index[service]
        
        if 'operations' not in service_data:
            return None
            
        if operation not in service_data['operations']:
            return None
            
        operation_data = service_data['operations'][operation]
        
        if 'params' not in operation_data:
            return None
            
        if param not in operation_data['params']:
            return None
            
        param_data = operation_data['params'][param]
        
        if 'completions' not in param_data:
            return None
            
        completion_data = param_data['completions']
        
        return ServerCompletion(
            operation=completion_data.get('operation'),
            path=completion_data.get('path'),
            params=completion_data.get('params', {})
        )