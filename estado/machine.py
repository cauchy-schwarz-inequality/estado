from collections import OrderedDict


class Machine:
    """ Class representing a state machine.
    """

    def __init__(self):
        self.states = OrderedDict()
        self.result = None

    def compile(self):
        """ Incrementally build a compiled state machine by calling
            the compile method of each state.
        """
        
        compiled = {
            "StartAt": self.start_at(),
            "States": {}
        }

        for state in self.states:
            compiled['States'] = {
                **compiled['States'],
                **self.states[state].compile()
            }

        return compiled

    def start_at(self):
        """ Obtain the name of the first state in the machine
        """ 
        return next(iter(self.states))

    def end_at(self):
        """ Obtain the name of the last state in the machine
        """
        return next(
            reversed(self.states.keys())
        )


    def last(self):
        """ Obtain the last state in the state machine
        """
        return self.states[
            next(reversed(
                self.states.keys()
            ))
        ]


    def register(self, state, force=False):
        """ Add a state to the state machine. If a state is added 
            sharing a name with a previously registered state, then 
            an exception will be raised.

            This function sets the next and end properties
            of the states registered. 

            TODO: Support manual configuration of state order properties
        """

        if state.name in self.states and not force:
            raise OperationalError(
                f"There is already a state named {state.name}" \
            )

        if self.states:
            self.states[self.end_at()].next = state.name
            self.states[self.end_at()].end = False

        state.end = True
        state.next = "End"

        self.states[state.name] = state


    def interpret(self, input=None):
        """ A naive interpretation function that simply passes the result 
            of the last state to the next state.
        """
        for state in self.states:
            # TODO: This call should take an input rather than result object
            self.result = self.states[state].interpret(input=input)
            input = self.result
        return self.result


    def __add__(self, other):
        """ Syntactic sugar allowing
              - A state to be registered using the + operator.
              - Two machines to be combined using the + operator.
           
            Let A and B be state machines, with a_1, a_2, a_3, ..., a_n states 
            of A, and b_1, b_2, b_3, ..., b_m states of B.

            Then the states of A + B will be ordered a_1 + ... + a_n + b_1 + ... + b_m,
            starting at state a_1 and with terminal state b_m.

            Note that this operation is associative but not commutative
        """
        from estado.state import State

        if isinstance(other, State):
            self.register(other)

        elif isinstance(other, Machine):
            for state in other.states:
                self += other.states[state]

        return self


class OperationalError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)

        
