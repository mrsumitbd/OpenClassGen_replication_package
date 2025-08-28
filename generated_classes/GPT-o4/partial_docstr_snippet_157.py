class NamespaceStatus(object):
    '''
    ``NamespaceStatus`` instances model `Kubernetes namespace status
    <https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_namespacestatus>`_.
    '''

    ACTIVE = 'Active'
    TERMINATING = 'Terminating'

    def __init__(self, phase):
        self.phase = phase

    @classmethod
    def active(cls):
        return cls(cls.ACTIVE)

    @classmethod
    def terminating(cls):
        return cls(cls.TERMINATING)

    def __eq__(self, other):
        if not isinstance(other, NamespaceStatus):
            return NotImplemented
        return self.phase == other.phase

    def __ne__(self, other):
        if not isinstance(other, NamespaceStatus):
            return NotImplemented
        return self.phase != other.phase

    def __repr__(self):
        return f'NamespaceStatus(phase={self.phase!r})'

    def __str__(self):
        return self.phase