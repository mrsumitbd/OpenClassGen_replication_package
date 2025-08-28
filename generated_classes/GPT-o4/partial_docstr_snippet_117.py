class RRELBase:

    def __init__(self):
        super().__init__()

    def get_next_matches(
        self, obj, lookup_list, allowed, matched_path, first_element=False
    ):
        if not allowed(obj, lookup_list, self):
            return

        try:
            next_objs = self.apply(obj)
        except AttributeError:
            # if subclass didn’t define apply
            return

        for next_obj in next_objs or ():
            yield next_obj, lookup_list