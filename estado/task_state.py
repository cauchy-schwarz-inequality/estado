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
            **self.compile_(),
            "Resource": self.resource
        }
        
        return {
            self.name: compiled
        }
        
