class BehaveHooksMixin:
    '''
    Provides methods that run during test execution.

    These methods are attached to behave via monkey patching.
    '''

    def patch_context(self, context):
        '''
        Patches the context to add utility functions

        Sets up the base_url, and the get_url() utility function.
        '''
        if hasattr(context, 'test') and hasattr(context.test, 'live_server_url'):
            context.base_url = context.test.live_server_url
        else:
            context.base_url = 'http://localhost:8000'
        
        def get_url(url_path=''):
            if url_path.startswith('/'):
                return context.base_url + url_path
            elif url_path:
                return context.base_url + '/' + url_path
            else:
                return context.base_url
        
        context.get_url = get_url

    def setup_testclass(self, context):
        '''
        Adds the test instance to context
        '''
        if not hasattr(context, 'test'):
            from django.test import TestCase
            context.test = TestCase()
            context.test._pre_setup()

    def setup_fixtures(self, context):
        '''
        Sets up fixtures
        '''
        if hasattr(context, 'test') and hasattr(context.test, '_fixture_setup'):
            context.test._fixture_setup()

    def teardown_test(self, context):
        '''
        Tears down the Django test
        '''
        if hasattr(context, 'test'):
            if hasattr(context.test, '_fixture_teardown'):
                context.test._fixture_teardown()
            if hasattr(context.test, '_post_teardown'):
                context.test._post_teardown()