class FaqEntryWrapper:
    def __init__(self, gs, entry):
        self.gs = gs
        self.entry = entry

    def __getattr__(self, k):
        return getattr(self.entry, k)

    @property
    def url(self):
        return f"/faq/{self.entry.id}"

    def render(self):
        return self.gs.render_template('faq_entry.html', entry=self)