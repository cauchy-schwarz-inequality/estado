class Machine:

    def __init__(self):
        self.states = {}
        self.result = None

    def compile(self, force=False):

        toplevel = {
            "StartAt": "",
            "States": {
            }
        }


        if not force:
            self.validate()

        return toplevel

    def validate(self):
        pass

    def register(self, state):
        self.states[state.name] = state
        

    def run(self):
        for state in self.states:
            self.result = self.states[state].run()
        return self.result

        
