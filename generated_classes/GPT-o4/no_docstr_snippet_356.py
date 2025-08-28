class DataframeJSON(object):
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = instance.__dict__.get(self.private_name, None)
        if isinstance(val, str):
            df = pd.read_json(val)
            instance.__dict__[self.private_name] = df
            return df
        return val

    def __set__(self, instance, encstr):
        if isinstance(encstr, str):
            df = pd.read_json(encstr)
        elif isinstance(encstr, pd.DataFrame):
            df = encstr
        else:
            raise TypeError("Value must be a JSON string or a pandas DataFrame")
        instance.__dict__[self.private_name] = df