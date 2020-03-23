from estado.hash_utils import slug_hash
from estado.input import Input
from estado.result import Result

SUPPORTED_STATE_TYPES = [
    "Pass",
    "Task"
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
        
        self.input = self.normalize_result_or_input(
            state_config.get("input"),
            Input
        )

        self.result = self.normalize_result_or_input(
            state_config.get("result"),
            Result
        )

        self.next = state_config.get("next")
        self.end = state_config.get("end", None)


    def normalize_result_or_input(self, result_or_input, Kind):
        """ In Estado, an input or result may be passed as a Python dictionary,
            an atomic type, or directly as an Input or Result object
        """
        if isinstance(result_or_input, dict):
            return Kind(
                **result_or_input
            )
        elif isinstance(result_or_input, Kind):
            return result_or_input
        else:
            return {
                Result: Result(result=result_or_input),
                Input: Input(input=result_or_input)
            }[Kind]


    def validate(self):
        """ Sanity checks validating that there isn't a conflict between 
            properties determining a state's terminal status and the 'next'
            property.
        """ 
        if self.terminal() and self.next:
            raise TerminalStateConflictException()

        if not self.terminal() and not self.next:
            raise TerminalStateConflictException(
                "State is not marked as end, but has no " \
                "next value specified"
            )                


    def compile_(self):
        """ Compilation logic common to each state type
        """
        compiled = {
            "Type": self.type,
        }

        if self.terminal():
            compiled["End"] = True
        else:
            compiled["Next"] = self.next
            compiled["End"] = False


        if self.result:
            compiled["Result"] = self.result.results
            compiled["ResultPath"] = self.result.path
        return compiled


    def terminal(self):
        """ Any state except for Choice, Succeed, and Fail MAY have a field 
            named "End" whose value MUST be a boolean. The term “Terminal State” 
            means a state with with { "End": true }, or a state with 
            { "Type": "Succeed" }, or a state with { "Type": "Fail" }.
        """
        return self.end or (self.type == "Succeed") or (self.type == "Fail")


    def __repr__(self):
        return f"<{self.type}:{self.name}>"


    def __add__(self, other):
        """ Syntactic sugar allowing states and machines to be combined
            using the + operator. 

            Let a_1 and b_1 be states. Then we can create a new state machine,
            a_1 + b_1, where a_1 is the initial state, and b_2 is the terminal state. 

            Now let M = m_1, m_2, ..., m_n be a machine. Then a_1 + M is a new state 
            machine with a_1 the initial state, m_1 the next state after a_1, 
            and m_n the terminal state. 
           
            Note that this operation is associative but not commutative
        """
        from estado.machine import Machine
        
        machine_ = Machine()
        machine_.register(self)

        if isinstance(other, State):
            machine_.register(other)
            
        elif isinstance(other, Machine):
            for state in other.states:
                machine_ += other.states[state]
                
        return machine_


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
