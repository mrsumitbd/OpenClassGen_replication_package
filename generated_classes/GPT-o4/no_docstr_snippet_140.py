class FaqEntryWrapper:
    def __init__(self, gs, entry):
        self.gs = gs
        self.entry = entry

    def __getattr__(self, k):
        try:
            return getattr(self.entry, k)
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{k}'")

    @property
    def url(self):
        base = getattr(self.gs, 'base_url', '')
        slug = getattr(self.entry, 'slug', '')
        return urljoin(base.rstrip('/') + '/', slug)

    def render(self):
        q = getattr(self.entry, 'question', '')
        a = getattr(self.entry, 'answer', '')
        return (
            f"<div class=\"faq-entry\">\n"
            f"  <h3><a href=\"{self.url}\">{q}</a></h3>\n"
            f"  <div class=\"faq-answer\">{a}</div>\n"
            f"</div>"
        )