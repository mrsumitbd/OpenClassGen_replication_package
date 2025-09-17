class BaseNewsItemChooserMixin:
    filterset_class = None

    def get_filterset_class(self):
        return self.filterset_class

    def get_filter_form_class(self):
        filterset_class = self.get_filterset_class()
        if not filterset_class:
            return None
        # django-filter ≥2.0
        form_cls = getattr(filterset_class, "form", None)
        if form_cls is not None:
            return form_cls
        # older django-filter
        return filterset_class.get_form_class()

    @property
    def columns(self):
        default = [
            ("title", "Title"),
            ("pub_date", "Publication Date"),
            ("author__username", "Author"),
        ]
        return getattr(self, "chooser_columns", default)