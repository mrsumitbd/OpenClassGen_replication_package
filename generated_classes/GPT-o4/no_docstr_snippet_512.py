class TemplateQueryGenerator(object):
    def __init__(self, template_finder):
        self.template_finder = template_finder

    def __call__(self, source, bounds, zoom):
        minx, miny, maxx, maxy = bounds
        template = self.template_finder(source, zoom)
        return template.format(
            source=source,
            minx=minx,
            miny=miny,
            maxx=maxx,
            maxy=maxy,
            zoom=zoom
        )