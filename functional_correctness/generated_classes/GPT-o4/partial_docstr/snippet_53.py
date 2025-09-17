class StructuredLogger:
    '''
    ABSTRACT BASE CLASS FOR JSON LOGGING
    '''

    def __init__(self, stream=None):
        self.stream = stream or sys.stdout

    def write(self, template, params):
        """
        Write a JSON log entry.
        template: str with format placeholders.
        params: dict of values to format into template and include in the record.
        """
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": template.format(**params) if params else template
        }
        if params:
            record.update(params)
        json.dump(record, self.stream)
        self.stream.write("\n")
        self.stream.flush()

    def stop(self):
        """Flush the stream."""
        try:
            self.stream.flush()
        except Exception:
            pass