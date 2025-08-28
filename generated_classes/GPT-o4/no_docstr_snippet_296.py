class Email:
    def __init__(self, data, manager):
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        self._data = data.copy()
        self._manager = manager

    def update(self):
        """
        Send current data to the manager for updating.
        The manager.update(...) method is expected to return
        a dict of updated fields (or None).
        """
        result = self._manager.update(self._data)
        if isinstance(result, dict):
            self._data.update(result)
        return self

    def delete(self):
        """
        Tell the manager to delete this email.
        The manager.delete(...) method may return a status or None.
        """
        return self._manager.delete(self._data.get("id"))

    def __str__(self):
        """
        A user‐friendly representation, showing key fields.
        """
        eid = self._data.get("id", "<no id>")
        subj = self._data.get("subject", "<no subject>")
        return f"<Email id={eid} subject={subj!r}>"

    def __repr__(self):
        """
        An unambiguous representation, suitable for debugging.
        """
        return f"Email(data={self._data!r})"