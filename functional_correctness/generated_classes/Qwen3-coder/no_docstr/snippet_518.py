class ACCESS_MASK(object):
    def __init__(self, mask):
        self.mask = mask

    def has_priv(self, priv):
        return bool(self.mask & priv)

    def set_priv(self, priv):
        self.mask |= priv

    def remove_priv(self, priv):
        self.mask &= ~priv

    def __repr__(self):
        return f"ACCESS_MASK({self.mask})"