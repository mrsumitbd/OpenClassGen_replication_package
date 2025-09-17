class GDPR:

    def __init__(self, app, sitemap, *args, **kwargs):
        self.app = app
        self.sitemap = sitemap
        self.args = args
        self.kwargs = kwargs
        if app is not None:
            self.init_app(app, sitemap, *args, **kwargs)

    def init_app(self, app, sitemap, *args, **kwargs):
        self.app = app
        self.sitemap = sitemap
        self.args = args
        self.kwargs = kwargs
        
        # Store reference to self in app for easy access
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        if 'gdpr' in app.extensions:
            raise RuntimeError("Flask application already initialized for GDPR")
        app.extensions['gdpr'] = self