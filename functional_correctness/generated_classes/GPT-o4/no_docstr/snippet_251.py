class _UuidSetValuesMixin(object):

    def _serialize_value(self, value_set):
        if value_set is None:
            return []
        return [str(u) for u in value_set]

    def _deserialize_value(self, data):
        if not data:
            return set()
        return {uuid.UUID(s) for s in data}