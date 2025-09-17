class ToDict:
    def __init__(self, data):
        self.data = data

    def setup(self, orient):
        if orient == 'ints':
            return self.time_to_dict_ints(orient)
        elif orient == 'datetimelike':
            return self.time_to_dict_datetimelike(orient)
        else:
            raise ValueError(f"Unknown orient: {orient!r}")

    def time_to_dict_ints(self, orient):
        result = {}
        for key, val in self.data.items():
            if hasattr(val, 'timestamp'):
                # datetime-like → epoch seconds as int
                result[key] = int(val.timestamp())
            else:
                result[key] = int(val)
        return result

    def time_to_dict_datetimelike(self, orient):
        result = {}
        for key, val in self.data.items():
            if isinstance(val, datetime):
                result[key] = val
            else:
                # assume numeric → convert from epoch seconds
                result[key] = datetime.fromtimestamp(int(val))
        return result