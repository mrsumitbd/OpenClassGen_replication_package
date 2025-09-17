class SliceContext(object):
    '''Context for map job.'''

    def __init__(self, shard_context, shard_state, tstate):
        '''Init.

        The signature of __init__ is subject to change.

        Read only properties:
          job_context: JobContext object.
          shard_context: ShardContext object.
          number: int. slice number. 0 indexed.
          attempt: int. The current attempt at executing this slice.
            starting at 1.

        Args:
          shard_context: map_job.JobConfig.
          shard_state: model.ShardState.
          tstate: model.TransientShardstate.
        '''
        self._shard_context = shard_context
        self._shard_state = shard_state
        self._tstate = tstate

    @property
    def job_context(self):
        return self._shard_context.job_context

    @property
    def shard_context(self):
        return self._shard_context

    @property
    def number(self):
        # slice number, 0-indexed
        return getattr(self._tstate, 'slice_number', None)

    @property
    def attempt(self):
        # current attempt at this slice, starting at 1
        return getattr(self._tstate, 'slice_attempt', None)

    def incr(self, counter_name, delta=1):
        '''See shard_context.count.'''
        return self._shard_context.count(counter_name, delta)

    def counter(self, counter_name, default=0):
        '''See shard_context.count.'''
        cnt = self._shard_context.count(counter_name)
        return default if cnt is None else cnt

    def emit(self, value):
        '''Emits a value to output writer.

        Args:
          value: a value of type expected by the output writer.
        '''
        # assume shard_context has an output writer attribute
        writer = getattr(self._shard_context, 'output_writer', None)
        if writer is None:
            writer = getattr(self._shard_context, 'writer', None)
        if writer is None:
            raise RuntimeError("No output writer available on shard_context")
        writer.write(value)