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
        host = context.config.userdata.get('host', 'localhost')
        port = context.config.userdata.get('port', 8000)
        context.base_url = f'http://{host}:{port}'

        def get_url(path):
            return urljoin(context.base_url, path)

        context.get_url = get_url

    def setup_testclass(self, context):
        '''
        Adds the test instance to context
        '''
        class BehaveTest(LiveServerTestCase):
            pass

        context.test = BehaveTest('runTest')

    def setup_fixtures(self, context):
        '''
        Sets up fixtures
        '''
        fixtures = context.config.userdata.get('fixtures', None)
        if fixtures:
            context.test.fixtures = fixtures
            context.test._fixture_setup()

    def setup_testclass(self, context):
        '''
        Sets up the Django test

        This method runs the code necessary to create the test database, start
        the live server, etc.
        '''
        cls = context.test.__class__
        cls.setUpClass()
        context.test.setUp()

    def teardown_test(self, context):
        '''
        Tears down the Django test
        '''
        context.test.tearDown()
        context.test.__class__.tearDownClass()