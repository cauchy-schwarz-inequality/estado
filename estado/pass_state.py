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


    def interpret(self):

        if not self.result:
            return self.input

        return self.result


    def compile(self):

        compiled = self.JSON_

        if self.terminal():
            compiled["Next"] = "End"
            compiled["End"] = self.end

        if self.result:
            compiled["Result"] = self.result.results
            compiled["ResultPath"] = self.result.path

        return {
            self.name: compiled
        }
        
