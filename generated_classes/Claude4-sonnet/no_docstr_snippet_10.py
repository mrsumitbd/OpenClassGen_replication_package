class base_case:
    def does_all_the_things(self, fakepub):
        return True

    def cleans_up_on_error(self, fakepub):
        try:
            fakepub.process()
        except Exception:
            fakepub.cleanup()
            raise

    def monkeypatches_readme_renderer(self, fakepub):
        import readme_renderer
        original_render = readme_renderer.render
        
        def patched_render(*args, **kwargs):
            return original_render(*args, **kwargs)
        
        readme_renderer.render = patched_render
        fakepub.readme_renderer = readme_renderer