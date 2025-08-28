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
        from django.conf import settings
        from django.urls import reverse
        
        context.base_url = getattr(settings, 'LIVE_SERVER_URL', 'http://localhost:8081')
        
        def get_url(url_name, *args, **kwargs):
            if url_name.startswith('/'):
                return context.base_url + url_name
            return context.base_url + reverse(url_name, args=args, kwargs=kwargs)
        
        context.get_url = get_url

    def setup_testclass(self, context):
        '''
        Adds the test instance to context
        '''
        from django.test import TestCase
        
        if not hasattr(self, '_test_instance'):
            self._test_instance = TestCase()
        context.test = self._test_instance

    def setup_fixtures(self, context):
        '''
        Sets up fixtures
        '''
        from django.core.management import call_command
        from django.db import connections
        from django.test.utils import setup_test_environment, teardown_test_environment
        
        setup_test_environment()
        
        # Create test database
        for connection in connections.all():
            connection.creation.create_test_db(autoclobber=True)
        
        # Load fixtures if specified
        if hasattr(self, 'fixtures'):
            call_command('loaddata', *self.fixtures, verbosity=0)

    def setup_testclass(self, context):
        '''
        Sets up the Django test

        This method runs the code necessary to create the test database, start
        the live server, etc.
        '''
        from django.test import LiveServerTestCase
        from django.test.utils import setup_test_environment
        
        setup_test_environment()
        
        if not hasattr(self, '_test_instance'):
            self._test_instance = LiveServerTestCase()
            self._test_instance._pre_setup()
        
        context.test = self._test_instance
        context.base_url = self._test_instance.live_server_url

    def teardown_test(self, context):
        '''
        Tears down the Django test
        '''
        from django.test.utils import teardown_test_environment
        from django.db import connections
        
        if hasattr(self, '_test_instance'):
            self._test_instance._post_teardown()
            delattr(self, '_test_instance')
        
        # Destroy test databases
        for connection in connections.all():
            connection.creation.destroy_test_db(connection.settings_dict['NAME'])
        
        teardown_test_environment()