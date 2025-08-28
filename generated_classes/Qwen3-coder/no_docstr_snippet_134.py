class DrawStyle(object):
    def __init__(self, styles=None, node_styles=[]):
        self.styles = styles if styles is not None else {}
        self.node_styles = node_styles.copy() if node_styles else []

    def __repr__(self):
        return f"DrawStyle(styles={self.styles}, node_styles={self.node_styles})"