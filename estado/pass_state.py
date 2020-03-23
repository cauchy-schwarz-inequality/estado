from estado.state import State


class Pass(State):

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

        if not self.result:
            self.result.results = self.input.inputs


    def interpret(self, input=None):
        if input:
            return input
        else:
            return self.result


    def compile(self):
        compiled = {
            "Type": "Pass",
            "Next": "End"
        }

        if self.terminal():
            compiled["Next"] = "End"
            compiled["End"] = self.end


        if self.result:
            compiled["Result"] = self.result.results
            compiled["ResultPath"] = self.result.path

        return {
            self.name: compiled
        }
        
