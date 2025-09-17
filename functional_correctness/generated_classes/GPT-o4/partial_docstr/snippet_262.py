class _FiniteStateMachine(object):
    def __init__(self, inputs, outputs, states, table, initial):
        # inputs, outputs, states: iterables of allowed constants
        # table: dict mapping state -> dict mapping input -> (output, nextState)
        self.inputs = set(inputs)
        self.outputs = set(outputs)
        self.states = set(states)
        if initial not in self.states:
            raise ValueError("Initial state %r not in states" % (initial,))
        # validate transition table
        if not isinstance(table, dict):
            raise TypeError("table must be a dict")
        for st, trans in table.items():
            if st not in self.states:
                raise ValueError("State %r in table not in declared states" % (st,))
            if not isinstance(trans, dict):
                raise TypeError("table[%r] must be a dict" % (st,))
            for inp, pair in trans.items():
                if inp not in self.inputs:
                    raise ValueError("Input %r not in declared inputs" % (inp,))
                if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
                    raise ValueError("Transition for %r->%r must be a (output,nextState) pair" % (st, inp))
                out, nxt = pair
                if out not in self.outputs:
                    raise ValueError("Output %r not in declared outputs" % (out,))
                if nxt not in self.states:
                    raise ValueError("Next state %r not in declared states" % (nxt,))
        self.table = {st: dict(trans) for st, trans in table.items()}
        self.initial = initial
        self.state = initial

    def receive(self, input):
        if input not in self.inputs:
            raise ValueError("Unrecognized input %r" % (input,))
        if self._isTerminal(self.state):
            raise RuntimeError("Cannot receive input in terminal state %r" % (self.state,))
        trans = self.table.get(self.state, {})
        if input not in trans:
            raise RuntimeError("No transition defined for state %r on input %r" % (self.state, input))
        output, nextstate = trans[input]
        # (output and nextstate were validated at init)
        self.state = nextstate
        return output

    def _isTerminal(self, state):
        '''
        Determine whether or not the given state is a terminal state in this
        state machine.  Terminal states have no transitions to other states.
        Additionally, terminal states have no outputs.
        '''
        trans = self.table.get(state)
        return not trans or len(trans) == 0