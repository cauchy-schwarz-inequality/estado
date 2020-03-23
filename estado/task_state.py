from estado.input import Input
from estado.result import Result
from estado.state import State


class Task(State):

    def __init__(self, name="", resource="",
                 registry=None, next=None,
                 end=False):

        state_config = {
            "name": name,
            "type": "Task",
            "next": next,
            "end": end
        }
            
        State.__init__(self, state_config)

        self.resource = resource
        self.registry = registry


    def interpret(self, input=None):

        if not input:
            input = Input()

        return Result(
            self.registry.invoke_function(
                self.resource,
                **input.inputs
            )
        )


    def compile(self):
        compiled = {
            "Type": "Task",
            "Resource": self.resource
        }

        if self.terminal():
            compiled["Next"] = "End"
            compiled["End"] = self.end
        else:
            compiled["Next"] = self.next
            compiled["End"] = False


        if self.result:
            compiled["Result"] = self.result.results
            compiled["ResultPath"] = self.result.path

        return {
            self.name: compiled
        }
        
