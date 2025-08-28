class DataframeJSON(object):
    def __init__(self, name=None):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, None)

    def __set__(self, instance, encstr):
        if isinstance(encstr, str):
            df = pd.read_json(encstr)
        elif isinstance(encstr, pd.DataFrame):
            df = encstr
        else:
            df = pd.DataFrame(encstr)
        setattr(instance, self.name, df)

    def __set_name__(self, owner, name):
        self.name = f'_{name}'