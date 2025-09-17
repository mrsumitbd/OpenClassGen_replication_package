class NamespaceStatus(object):
    '''
    ``NamespaceStatus`` instances model `Kubernetes namespace status
    <https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_namespacestatus>`_.
    '''

    def __init__(self, phase):
        self.phase = phase

    @classmethod
    def active(cls):
        return cls("Active")

    @classmethod
    def terminating(cls):
        return cls("Terminating")

    def __eq__(self, other):
        if not isinstance(other, NamespaceStatus):
            return False
        return self.phase == other.phase

    def __hash__(self):
        return hash(self.phase)

    def __repr__(self):
        return f"NamespaceStatus(phase='{self.phase}')"