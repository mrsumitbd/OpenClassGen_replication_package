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
        params = {}
        for name, transformer in self.steps:
            if hasattr(transformer, 'get_params'):
                params[name] = transformer.get_params()
            else:
                params[name] = transformer
        return params

    def __repr__(self):
        '''Pretty-print the object'''
        step_strs = []
        for name, transformer in self.steps:
            step_strs.append(f"('{name}', {repr(transformer)})")
        return f"Pipeline(steps=[{', '.join(step_strs)}])"

    def __recursive_transform(self, jam, steps):
        '''A recursive transformation pipeline'''
        if not steps:
            yield jam
        else:
            name, transformer = steps[0]
            remaining_steps = steps[1:]
            for transformed_jam in transformer.transform(jam):
                yield from self.__recursive_transform(transformed_jam, remaining_steps)

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
        yield from self.__recursive_transform(jam, self.steps)