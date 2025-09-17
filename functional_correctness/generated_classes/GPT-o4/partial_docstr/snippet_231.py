class WorkerStats:
    ''' Represents the worker information returned from celery.

    Args:
        name (str): The name of the worker.
        broker (BrokerStats): A reference to a BrokerStats Object the worker is using.
        pid (int): The PID of the worker.
        process_pids (int): The PIDs of the concurrent task processes.
        concurrency (int): The number of concurrent processes.
        job_count (int): The number of jobs this worker has processed so far.
        queues (list): A list of QueueStats objects that represent the queues this
            worker is listening on.
    '''

    def __init__(self, name, broker, pid, process_pids,
                 concurrency, job_count, queues):
        self.name = name
        self.broker = broker
        self.pid = pid
        self.process_pids = process_pids
        self.concurrency = concurrency
        self.job_count = job_count
        self.queues = queues

    @classmethod
    def from_celery(cls, name, worker_dict, queues):
        ''' Create a WorkerStats object from the dictionary returned by celery.

            Args:
                name (str): The name of the worker.
                worker_dict (dict): The dictionary as returned by celery.
                queues (list): A list of QueueStats objects that represent the queues this
                    worker is listening on.

            Returns:
                WorkerStats: A fully initialized WorkerStats object.
        '''
        broker = worker_dict.get('broker')
        pid = worker_dict.get('pid')
        # celery may report processes under 'processes' or 'pool' -> 'processes'
        process_pids = worker_dict.get('processes') \
                       or worker_dict.get('pool', {}).get('processes', [])
        # celery may report concurrency under 'concurrency' or 'pool' -> 'max-concurrency'
        concurrency = worker_dict.get('concurrency') \
                      or worker_dict.get('pool', {}).get('max-concurrency')
        # celery may report total tasks processed under 'total' or 'job_count'
        job_count = worker_dict.get('total') or worker_dict.get('job_count', 0)

        return cls(name, broker, pid, process_pids, concurrency, job_count, queues)

    def to_dict(self):
        ''' Return a dictionary of the worker stats.

            Returns:
                dict: Dictionary of the stats.
        '''
        return {
            'name': self.name,
            'broker': getattr(self.broker, 'to_dict', lambda: self.broker)(),
            'pid': self.pid,
            'process_pids': list(self.process_pids),
            'concurrency': self.concurrency,
            'job_count': self.job_count,
            'queues': [q.to_dict() for q in self.queues],
        }