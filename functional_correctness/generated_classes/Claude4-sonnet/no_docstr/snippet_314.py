class GDPR:
    def __init__(self, app=None, sitemap=None, *args, **kwargs):
        self.app = app
        self.sitemap = sitemap
        self.config = {}
        self.consent_types = ['necessary', 'analytics', 'marketing', 'preferences']
        self.cookie_banner_template = None
        self.privacy_policy_url = None
        self.cookie_policy_url = None
        self.consent_storage_key = 'gdpr_consent'
        
        if app is not None:
            self.init_app(app, sitemap, *args, **kwargs)

    def init_app(self, app, sitemap=None, *args, **kwargs):
        self.app = app
        if sitemap is not None:
            self.sitemap = sitemap
            
        # Set default configuration
        app.config.setdefault('GDPR_COOKIE_BANNER_ENABLED', True)
        app.config.setdefault('GDPR_CONSENT_REQUIRED', True)
        app.config.setdefault('GDPR_COOKIE_DOMAIN', None)
        app.config.setdefault('GDPR_COOKIE_SECURE', False)
        app.config.setdefault('GDPR_COOKIE_HTTPONLY', True)
        app.config.setdefault('GDPR_COOKIE_SAMESITE', 'Lax')
        app.config.setdefault('GDPR_CONSENT_EXPIRY_DAYS', 365)
        
        # Store configuration
        self.config.update(app.config)
        
        # Register template globals
        app.jinja_env.globals['gdpr'] = self
        
        # Register routes
        self._register_routes(app)
        
        # Add to app extensions
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['gdpr'] = self

    def _register_routes(self, app):
        @app.route('/gdpr/consent', methods=['POST'])
        def set_consent():
            from flask import request, jsonify, make_response
            consent_data = request.get_json()
            response = make_response(jsonify({'status': 'success'}))
            
            cookie_options = {
                'max_age': self.config.get('GDPR_CONSENT_EXPIRY_DAYS', 365) * 24 * 60 * 60,
                'secure': self.config.get('GDPR_COOKIE_SECURE', False),
                'httponly': self.config.get('GDPR_COOKIE_HTTPONLY', True),
                'samesite': self.config.get('GDPR_COOKIE_SAMESITE', 'Lax')
            }
            
            if self.config.get('GDPR_COOKIE_DOMAIN'):
                cookie_options['domain'] = self.config['GDPR_COOKIE_DOMAIN']
            
            import json
            response.set_cookie(self.consent_storage_key, json.dumps(consent_data), **cookie_options)
            return response
        
        @app.route('/gdpr/consent', methods=['GET'])
        def get_consent():
            from flask import request, jsonify
            import json
            consent_cookie = request.cookies.get(self.consent_storage_key)
            if consent_cookie:
                try:
                    consent_data = json.loads(consent_cookie)
                    return jsonify(consent_data)
                except json.JSONDecodeError:
                    pass
            return jsonify({})

    def has_consent(self, consent_type='necessary'):
        from flask import request
        import json
        consent_cookie = request.cookies.get(self.consent_storage_key)
        if consent_cookie:
            try:
                consent_data = json.loads(consent_cookie)
                return consent_data.get(consent_type, False)
            except json.JSONDecodeError:
                pass
        return consent_type == 'necessary'

    def require_consent(self, consent_type):
        def decorator(f):
            from functools import wraps
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not self.has_consent(consent_type):
                    from flask import abort
                    abort(403)
                return f(*args, **kwargs)
            return decorated_function
        return decorator

    def get_consent_banner_html(self):
        if self.cookie_banner_template:
            from flask import render_template
            return render_template(self.cookie_banner_template, gdpr=self)
        return self._default_banner_html()

    def _default_banner_html(self):
        return '''
        <div id="gdpr-banner" style="position: fixed; bottom: 0; left: 0; right: 0; background: #333; color: white; padding: 20px; z-index: 9999;">
            <p>This website uses cookies to ensure you get the best experience. 
            <a href="#" onclick="acceptAllCookies()">Accept All</a> | 
            <a href="#" onclick="showCookieSettings()">Cookie Settings</a></p>
        </div>
        <script>
        function acceptAllCookies() {
            fetch('/gdpr/consent', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({necessary: true, analytics: true, marketing: true, preferences: true})
            }).then(() => document.getElementById('gdpr-banner').style.display = 'none');
        }
        </script>
        '''