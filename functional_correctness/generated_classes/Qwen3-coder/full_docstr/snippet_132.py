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
        return self._tstate.slice_id

    @property
    def attempt(self):
        return self._tstate.retry_count + 1

    def incr(self, counter_name, delta=1):
        '''See shard_context.count.'''
        self._shard_context.incr(counter_name, delta)

    def counter(self, counter_name, default=0):
        '''See shard_context.count.'''
        return self._shard_context.counter(counter_name, default)

    def emit(self, value):
        '''Emits a value to output writer.

        Args:
          value: a value of type expected by the output writer.
        '''
        self._tstate.output_writer.write(value)