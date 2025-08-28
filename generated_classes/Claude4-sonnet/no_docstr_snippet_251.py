class _UuidSetValuesMixin(object):

    def _serialize_value(self, value_set):
        if value_set is None:
            return None
        return [str(uuid_val) for uuid_val in value_set]

    def _deserialize_value(self, data):
        if data is None:
            return None
        return {uuid.UUID(uuid_str) for uuid_str in data}