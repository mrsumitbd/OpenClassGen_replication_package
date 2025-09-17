class GDPR:

    def __init__(self, app=None, sitemap=None, *args, **kwargs):
        self.app = None
        self.sitemap = None
        if app is not None:
            self.init_app(app, sitemap, *args, **kwargs)

    def init_app(self, app, sitemap, *args, **kwargs):
        self.app = app
        self.sitemap = sitemap
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['gdpr'] = self
        return self