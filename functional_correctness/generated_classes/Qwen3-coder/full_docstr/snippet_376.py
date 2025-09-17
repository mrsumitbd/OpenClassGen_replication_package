class Edge:
    '''A connecting edge for a lineage graph.'''

    def __init__(
        self,
        source_arn: str,
        destination_arn: str,
        association_type: str,
    ):
        '''Initialize ``Edge`` instance.'''
        self.source_arn = source_arn
        self.destination_arn = destination_arn
        self.association_type = association_type

    def __hash__(self):
        '''Define hash function for ``Edge``.'''
        return hash((self.source_arn, self.destination_arn, self.association_type))

    def __eq__(self, other):
        '''Define equal function for ``Edge``.'''
        if not isinstance(other, Edge):
            return False
        return (self.source_arn == other.source_arn and
                self.destination_arn == other.destination_arn and
                self.association_type == other.association_type)

    def __str__(self):
        '''Define string representation of ``Edge``.

        Format:
            {
                'source_arn': 'string',
                'destination_arn': 'string',
                'association_type': 'string'
            }

        '''
        return str({
            'source_arn': self.source_arn,
            'destination_arn': self.destination_arn,
            'association_type': self.association_type
        })

    def __repr__(self):
        '''Define string representation of ``Edge``.

        Format:
            {
                'source_arn': 'string',
                'destination_arn': 'string',
                'association_type': 'string'
            }

        '''
        return str({
            'source_arn': self.source_arn,
            'destination_arn': self.destination_arn,
            'association_type': self.association_type
        })