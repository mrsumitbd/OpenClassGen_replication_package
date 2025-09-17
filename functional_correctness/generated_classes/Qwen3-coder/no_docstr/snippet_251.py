class _UuidSetValuesMixin(object):

    def _serialize_value(self, value_set):
        if value_set is None:
            return None
        return [str(uuid) for uuid in value_set]

    def _deserialize_value(self, data):
        if data is None:
            return None
        import uuid
        return {uuid.UUID(item) for item in data}