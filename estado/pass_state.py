from estado.state import State


class Pass(State):

    JSON_ = {
        "Type": "Pass",
        "Next": "End"
    }

    def __init__(self, result=None, name="",
                 next=None, end=False, **input):

        state_config = {
            "name": name,
            "type": "Pass",
            "next": next,
            "input": input,
            "result": result,
            "end": end
        }
            
        State.__init__(self, state_config)


    def run(self):

        if not self.result:
            return self.input

        return self.result
