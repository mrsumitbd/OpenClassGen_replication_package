class base_case:

    def does_all_the_things(self, fakepub):
        self.monkeypatches_readme_renderer(fakepub)
        try:
            fakepub.setup_project()
            fakepub.build_sdist()
            fakepub.build_wheel()
            fakepub.upload()
        except Exception:
            self.cleans_up_on_error(fakepub)
            raise

    def cleans_up_on_error(self, fakepub):
        # remove temporary build directories if they exist
        for attr in ("sdist_dir", "wheel_dir", "build_dir"):
            path = getattr(fakepub, attr, None)
            if path and os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)

    def monkeypatches_readme_renderer(self, fakepub):
        import readme_renderer.rst
        fakepub.monkeypatch.setattr(
            readme_renderer.rst,
            "render",
            lambda text, **kwargs: ("<p>%s</p>" % text, [])
        )