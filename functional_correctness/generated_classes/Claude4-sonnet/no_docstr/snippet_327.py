class LeaderboardEntry(object):

    def __init__(self, init_dict):
        for key, value in init_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = []
        for key, value in self.__dict__.items():
            if isinstance(value, str):
                attrs.append(f"{key}='{value}'")
            else:
                attrs.append(f"{key}={value}")
        return f"LeaderboardEntry({', '.join(attrs)})"