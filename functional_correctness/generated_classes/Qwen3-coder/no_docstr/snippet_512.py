class TemplateQueryGenerator(object):

    def __init__(self, template_finder):
        self.template_finder = template_finder

    def __call__(self, source, bounds, zoom):
        template = self.template_finder(source, bounds, zoom)
        if template is None:
            return None
        return template.query(bounds, zoom)