class DataframeJSON(object):
    
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        data = instance.__dict__.get(self.name)
        if data is not None:
            return pd.DataFrame(data)
        return None

    def __set__(self, instance, encstr):
        if encstr is None:
            instance.__dict__[self.name] = None
        else:
            if isinstance(encstr, pd.DataFrame):
                instance.__dict__[self.name] = encstr.to_dict('records')
            elif isinstance(encstr, str):
                instance.__dict__[self.name] = json.loads(encstr)
            else:
                instance.__dict__[self.name] = encstr