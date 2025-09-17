class BaseNewsItemChooserMixin:

    def get_filter_form_class(self):
        raise NotImplementedError("Subclasses must implement get_filter_form_class method")

    def get_filter_form_class(self):
        raise NotImplementedError("Subclasses must implement get_filter_form_class method")

    @property
    def columns(self):
        raise NotImplementedError("Subclasses must implement columns property")