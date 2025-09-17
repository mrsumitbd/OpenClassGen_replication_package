class Progress:
    '''
    An interface for receiving events that occur during the execution of the
    TidyPy tool suite.
    '''

    def __init__(self):
        self._suite_start = None
        self._suite_end = None
        self._tool_start_times = {}
        self._tool_durations = {}

    def on_start(self):
        '''
        Called when the execution of the TidyPy tool suite begins.
        '''
        self._suite_start = time.time()
        print("TidyPy suite starting...")

    def on_tool_start(self, tool):
        '''
        Called when an individual tool begins execution.

        :param tool: the name of the tool that is starting
        :type tool: str
        '''
        self._tool_start_times[tool] = time.time()
        print(f"  [START] Tool '{tool}'")

    def on_tool_finish(self, tool):
        '''
        Called when an individual tool completes execution.

        :param tool: the name of the tool that completed
        :type tool: str
        '''
        start = self._tool_start_times.get(tool)
        if start is None:
            print(f"  [WARNING] Finished '{tool}' without start time")
            return
        end = time.time()
        duration = end - start
        self._tool_durations[tool] = duration
        print(f"  [DONE ] Tool '{tool}' finished in {duration:.2f}s")

    def on_finish(self):
        '''
        Called after all tools in the suite have completed.
        '''
        self._suite_end = time.time()
        total_suite = self._suite_end - self._suite_start if self._suite_start else 0
        print("TidyPy suite finished.")
        print(f"Total suite time: {total_suite:.2f}s")
        if self._tool_durations:
            print("Tool summary:")
            for tool, dur in self._tool_durations.items():
                print(f"  - {tool}: {dur:.2f}s")