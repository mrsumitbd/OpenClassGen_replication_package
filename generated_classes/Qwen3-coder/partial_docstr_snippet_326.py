class Pipeline(object):
    '''Wrapper which allows multiple BaseDeformer objects to be chained together

    A given JAMS object will be transformed sequentially by
    each stage of the pipeline.

    The pipeline induces a graph over transformers

    Attributes
    ----------
    steps : argument array
        steps[i] is a tuple of `(name, Transformer)`

    Examples
    --------
    >>> P = muda.deformers.PitchShift(semitones=5)
    >>> T = muda.deformers.TimeStretch(speed=1.25)
    >>> Pipe = muda.Pipeline(steps=[('Pitch:maj3', P), ('Speed:1.25x', T)])
    >>> output_jams = list(Pipe.transform(jam_in))

    See Also
    --------
    Union
    '''

    def __init__(self, steps=None):
        if steps is None:
            steps = []
        self.steps = steps

    def get_params(self):
        '''Get the parameters for this object.  Returns as a dict.'''
        return {'steps': [(name, transformer.get_params()) for name, transformer in self.steps]}

    def __repr__(self):
        '''Pretty-print the object'''
        repr_str = '{}(steps=[{}])'.format(
            self.__class__.__name__,
            ', '.join('("{}", {})'.format(name, repr(transformer)) for name, transformer in self.steps)
        )
        return repr_str

    def __recursive_transform(self, jam, steps):
        '''A recursive transformation pipeline'''
        if not steps:
            yield jam
        else:
            name, transformer = steps[0]
            for transformed_jam in transformer.transform(jam):
                for result_jam in self.__recursive_transform(transformed_jam, steps[1:]):
                    yield result_jam

    def transform(self, jam):
        '''Apply the sequence of transformations to a single jam object.

        Parameters
        ----------
        jam : jams.JAMS
            The jam object to transform

        Yields
        ------
        jam_out : jams.JAMS
            The jam objects produced by the transformation sequence
        '''
        for result in self.__recursive_transform(jam, self.steps):
            yield result