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

        if not force:
            self.validate()

        for state in self.states:

            compiled['States'] = {
                **compiled['States'],
                **self.states[state].compile()
            }

        return compiled

    def start_at(self):
        return next(iter(self.states))

    def validate(self):
        pass

    def register(self, state):
        self.states[state.name] = state
        

    def interpret(self):
        for state in self.states:
            self.result = self.states[state].interpret()
        return self.result

        
