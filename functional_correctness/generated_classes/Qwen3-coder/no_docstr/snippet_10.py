class base_case:


    def does_all_the_things(self, fakepub):
        # Implementation for doing all the things
        if fakepub is not None:
            fakepub.process()
            fakepub.validate()
            fakepub.publish()
            return True
        return False


    def cleans_up_on_error(self, fakepub):
        # Implementation for cleaning up on error
        try:
            if fakepub is not None:
                fakepub.process()
        except Exception as e:
            if fakepub is not None:
                fakepub.cleanup()
            raise e


    def monkeypatches_readme_renderer(self, fakepub):
        # Implementation for monkeypatching readme renderer
        if fakepub is not None:
            original_render = fakepub.render_readme
            fakepub.render_readme = lambda content: f"PATCHED: {original_render(content)}"
            return fakepub.render_readme
        return None