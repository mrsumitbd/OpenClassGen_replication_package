class TemplateQueryGenerator(object):

    def __init__(self, template_finder):
        self.template_finder = template_finder

    def __call__(self, source, bounds, zoom):
        template = self.template_finder(source, bounds, zoom)
        if template is None:
            return None
        
        # Extract bounds coordinates
        minx, miny, maxx, maxy = bounds
        
        # Create substitution dictionary
        substitutions = {
            'minx': minx,
            'miny': miny,
            'maxx': maxx,
            'maxy': maxy,
            'zoom': zoom,
            'source': source
        }
        
        # Perform template substitution
        try:
            query = template.format(**substitutions)
            return query
        except (KeyError, ValueError):
            return template