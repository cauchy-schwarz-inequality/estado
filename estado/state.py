from estado.hash_utils import slug_hash
from estado.result import Result

SUPPORTED_STATE_TYPES = [
    "Pass"
]

class State:

    def __init__(self, state_config):

        type_ = state_config["type"]

        if type_ not in SUPPORTED_STATE_TYPES:
            raise InvalidStateTypeException(type_)

        self.type = type_


        name = state_config.get("name")

        if not name:
            self.name = slug_hash()
        else:
            self.name = name
        
        self.input = state_config.get("input")

        self.result = self.normalize_result(
            state_config.get("result")
        )


        self.next = state_config.get("next")
        self.end = state_config.get("end", None)


    def normalize_result(self, result):
        if isinstance(result, dict):
            return Result(
                **result
            )
        elif isinstance(result, Result):
            return result
        else:
            return Result(result=result)


    def compile(self):

        # TODO: This will blow up on the first error.
        # A more useful compiler would try to keep going and
        # let us know about all failed validations. 

        if self.terminal() and self.next:
            raise TerminalStateConflictException()

        if not self.terminal() and not self.next:
            raise TerminalStateConflictException(
                "State is not marked as end, but has no " \
                "next value specified"
            )


    def terminal(self):
        """
        Any state except for Choice, Succeed, and Fail MAY have a field 
        named "End" whose value MUST be a boolean. The term “Terminal State” 
        means a state with with { "End": true }, or a state with 
        { "Type": "Succeed" }, or a state with { "Type": "Fail" }.
        """
        return self.end or (self.type == "Succeed") or (self.type == "Fail") or self.next == "End"


    def __repr__(self):
        return f"<{self.type}:{self.name}>"


class InvalidStateTypeException(Exception):

    def __init__(self, type_):
        message = f"State type {type_} not supported" \
        f"State type should be one of \n" \
        f"{SUPPORTED_STATE_TYPES}"
        Exception.__init__(self, message)
        

class TerminalStateConflictException(Exception):

    def __init__(self, message=""):
        if not message:
            message = "Next cannot have a non-null value" \
                "when a state has a terminal marker."
        Exception.__init__(self, message)
