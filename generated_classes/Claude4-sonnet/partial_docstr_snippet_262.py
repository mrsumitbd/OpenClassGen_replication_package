class _FiniteStateMachine(object):
    '''
    A L{_FiniteStateMachine} tracks the core logic of a finite state machine:
    recording the current state and mapping inputs to outputs and next states.

    @ivar inputs: See L{constructFiniteStateMachine}
    @ivar outputs: See L{constructFiniteStateMachine}
    @ivar states: See L{constructFiniteStateMachine}
    @ivar table: See L{constructFiniteStateMachine}
    @ivar initial: See L{constructFiniteStateMachine}

    @ivar state: The current state of this FSM.
    @type state: L{NamedConstant} from C{states}
    '''

    def __init__(self, inputs, outputs, states, table, initial):
        self.inputs = inputs
        self.outputs = outputs
        self.states = states
        self.table = table
        self.initial = initial
        self.state = initial

    def receive(self, input):
        if self.state in self.table and input in self.table[self.state]:
            output, next_state = self.table[self.state][input]
            self.state = next_state
            return output
        else:
            raise ValueError("Invalid input for current state")

    def _isTerminal(self, state):
        '''
        Determine whether or not the given state is a terminal state in this
        state machine.  Terminal states have no transitions to other states.
        Additionally, terminal states have no outputs.

        @param state: The state to examine.

        @return: C{True} if the state is terminal, C{False} if it is not.
        @rtype: L{bool}
        '''
        return state not in self.table or len(self.table[state]) == 0