class LeaderboardEntry(object):

    def __init__(self, init_dict):
        if not isinstance(init_dict, dict):
            raise TypeError("init_dict must be a dict")
        for key, value in init_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        items = sorted(self.__dict__.items())
        body = ", ".join(f"{k}={v!r}" for k, v in items)
        return f"{self.__class__.__name__}({body})"