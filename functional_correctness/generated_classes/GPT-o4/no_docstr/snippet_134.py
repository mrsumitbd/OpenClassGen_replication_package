class DrawStyle(object):
    def __init__(self, styles=None, node_styles=[]):
        # Initialize styles dictionary
        if styles is None:
            self.styles = {}
        elif isinstance(styles, dict):
            self.styles = styles.copy()
        else:
            try:
                self.styles = dict(styles)
            except Exception:
                raise TypeError("styles must be a dict or iterable of key/value pairs")

        # Initialize node_styles list of dicts
        self.node_styles = []
        for ns in node_styles:
            if isinstance(ns, dict):
                self.node_styles.append(ns.copy())
            else:
                try:
                    self.node_styles.append(dict(ns))
                except Exception:
                    raise TypeError("each node_style must be a dict or iterable of key/value pairs")

    def __repr__(self):
        return "{}(styles={!r}, node_styles={!r})".format(
            self.__class__.__name__, self.styles, self.node_styles
        )