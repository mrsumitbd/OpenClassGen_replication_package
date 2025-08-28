class FaqEntryWrapper:
    def __init__(self, gs, entry):
        self.gs = gs
        self.entry = entry

    def __getattr__(self, k):
        return getattr(self.entry, k)

    @property
    def url(self):
        return f"{self.gs.base_url}/faq/{self.entry.id}"

    def render(self):
        return f"<div class='faq-entry'><h3>{self.entry.question}</h3><p>{self.entry.answer}</p></div>"