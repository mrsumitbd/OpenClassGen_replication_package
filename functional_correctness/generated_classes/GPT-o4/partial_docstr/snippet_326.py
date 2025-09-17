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
        if not isinstance(steps, (list, tuple)):
            raise ValueError("`steps` must be a list or tuple of (name, transformer) pairs")
        for s in steps:
            if not (isinstance(s, (list, tuple)) and len(s) == 2):
                raise ValueError("Each step must be a (name, transformer) tuple")
        self.steps = list(steps)

    def get_params(self):
        '''Get the parameters for this object.  Returns as a dict.'''
        params = {}
        params['steps'] = []
        for name, transformer in self.steps:
            if hasattr(transformer, 'get_params'):
                params['steps'].append((name, transformer.get_params()))
            else:
                params['steps'].append((name, None))
        return params

    def __repr__(self):
        '''Pretty-print the object'''
        step_reprs = []
        for name, transformer in self.steps:
            step_reprs.append(f"('{name}', {transformer!r})")
        steps_str = '[' + ', '.join(step_reprs) + ']'
        return f"{self.__class__.__name__}(steps={steps_str})"

    def __recursive_transform(self, jam, steps):
        '''A recursive transformation pipeline'''
        if not steps:
            yield jam
            return
        name, transformer = steps[0]
        for jam_out in transformer.transform(jam):
            yield from self.__recursive_transform(jam_out, steps[1:])

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