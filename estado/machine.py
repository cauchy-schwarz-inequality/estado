from collections import OrderedDict

class Machine:

    def __init__(self):
        self.states = OrderedDict()
        self.result = None

    def compile(self, force=False):

        compiled = {
            "StartAt": self.start_at(),
            "States": {
            }
        }


        for state in self.states:

            compiled['States'] = {
                **compiled['States'],
                **self.states[state].compile()
            }

        return compiled

    def start_at(self):
        """ Obtain the name of the first state
        """ 
        return next(iter(self.states))

    def end_at(self):
        return next(
            reversed(self.states.keys())
        )

    def last(self):
        """ Obtain the last state
        """
        return self.states[
            next(reversed(
                self.states.keys()
            ))
        ]


    def register(self, state, force=False):

        if state.name in self.states and not force:
            raise OperationalError(
                f"There is already a state named {state.name}" \
            )

        if self.states:
            last_state = self.last()
            last_state.next = state.name
            last_state.end = False

        state.end = True
        state.next = "End"

        self.states[state.name] = state


    def interpret(self, input=None):
        for state in self.states:
            self.result = self.states[state].interpret(input=input)
            input = self.result
        return self.result


class OperationalError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)

        
