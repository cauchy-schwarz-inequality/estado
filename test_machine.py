from estado.machine import Machine, OperationalError
from estado.input import Input
from estado.pass_state import Pass
from estado.result  import Result
from estado.resource_registry import Registry
from estado.state import InvalidStateTypeException, TerminalStateConflictException
from estado.state import State
from estado.task_state import Task

import pytest


def test_toplevel():
    """
    A State Machine MUST have an object field named “States”, whose fields represent the states.

    A State Machine MUST have a string field named “StartAt”, whose value MUST exactly match one of names of the “States” fields. 
    The interpreter starts running the the machine at the named state.
    """
    
    machine = Machine()
    machine.register(Pass())
    compiled = machine.compile()
    
    assert "States" in compiled
    assert "StartAt" in compiled


def test_pass_state():
    """
    The Pass State (identified by "Type":"Pass") simply passes its input to its output, performing no work. 

    A Pass State MAY have a field named “Result”. 

    If present, its value is treated as the output of a virtual task, and placed as prescribed by the “ResultPath” field, 
    if any, to be passed on to the next state. 

    If “Result” is not provided, the output is the input. 

    Thus if neither “Result” nor “ResultPath” are provided, the Pass state copies its input through to its output.
    """
    
    machine = Machine()
    pass_ = Pass(2)
    machine.register(pass_)
    pass_run_result = machine.interpret()

    assert pass_run_result == 2

    pass_ = Pass(result=5)
    machine_2 = Machine()
    machine_2.register(pass_)
    pass_2_run_result = machine_2.interpret()

    assert pass_2_run_result == 5


def test_result_equality():

    assert Result(2) == 2

    assert Result(2) == {"result": 2}

    assert Result() == None


    result_data = {
        "a": 1,
        "b": 2,
        "c": 3
    }
    lhs = Result(result_data)
    rhs = Result(result_data)

    assert lhs == rhs

def test_invalid_state_type_raises_exception():
    state_config = {
        "type": "Some unsupported state type"
    }
    with pytest.raises(InvalidStateTypeException):
        state = State(state_config)


def test_conflicting_terminal_state_raises_exception():
    state_config = {
        "type": "Pass",
        "end": True,
        "next": "A non-null next value"
    }

    state = State(state_config)

    with pytest.raises(TerminalStateConflictException):
        state.validate()
    

def test_compile_pass_state():

    pass_expected = {
        "No-op": {
            "Type": "Pass",
            "Result": {
                "x": 0.381018,
                "y": 622.2269926397355
            },
            "Next": "End",
            "End": True,
            "ResultPath": "$.result"
        }
    }

    result = Result(
        x=0.381018,
        y=622.2269926397355
    )

    pass_ = Pass(
        result=result,
        name="No-op",
        end=True
    )

    assert pass_.compile() == pass_expected

    machine = Machine()
    machine.register(pass_)

    assert machine.interpret() == result

    compiled_machine_expected = {
        "StartAt": "No-op",
        "States": {
            "No-op": {
                "Type": "Pass",
                "Result": {
                    "x": 0.381018,
                    "y": 622.2269926397355
                },
                "Next": "End",
                "End": True,
                "ResultPath": "$.result"
            }
        }
    }

    assert machine.compile() == compiled_machine_expected

    
def test_duplicate_statename_triggers_operationalerror():

    first_state = Pass(name="test_state")
    second_state = Pass(name="test_state")

    machine = Machine()
    machine.register(first_state)

    with pytest.raises(OperationalError):
        machine.register(second_state)


def test_register_duplicate_statename_with_force():

    first_state = Pass(name="test_state")
    second_state = Pass(name="test_state")

    machine = Machine()
    machine.register(first_state)
    machine.register(second_state, force=True)

    compiled = machine.compile()

    expected = {
        "StartAt": "test_state",
        "States": {
            "test_state": {
                "Type": "Pass",
                "Next": "End",
                "End": True
            }
        }
    }

    assert compiled == expected
    

def test_pass_state_transition():

    first_state = Pass(name="state_one")
    second_state = Pass(name="state_two")

    machine = Machine()
    machine.register(first_state)
    machine.register(second_state)

    assert machine.start_at() == "state_one"
    assert machine.end_at() == "state_two"
    assert machine.last().terminal()

    assert machine.interpret(52) == 52

    compiled = machine.compile()

    expected = {
        "StartAt": "state_one",
        "States": {
            "state_one": {
                "Type": "Pass",
                "Next": "state_two",
                "End": False
            },
            "state_two": {
                "Type": "Pass",
                "Next": "End",
                "End": True
            }
            
        }
    }

    assert compiled == expected


@pytest.fixture
def registry():
    fn_registry = Registry()

    add_two = lambda x: x + 2
    add_two_args = lambda x, y: x + y

    def add_with_defaults(x=1,y=5):
        return x + y

    fn_registry.register_function(add_two, "add_two")
    fn_registry.register_function(add_two_args, "add_two_args")
    fn_registry.register_function(add_with_defaults, "add_with_defaults")

    return fn_registry


def test_resource_registry(registry):

    assert registry.invoke_function("add_two", x=1) == 3
    assert registry.invoke_function("add_two_args", x=50, y=50) == 100
    assert registry.invoke_function("add_with_defaults") == 6
    assert registry.invoke_function("add_two", **{"x": 1}) == 3


def test_interpret_single_task(registry):

    task = Task(
        name="test_task",
        resource="add_with_defaults",
        registry=registry
    )

    assert task.interpret() == 6

    machine = Machine()
    machine.register(task)

    assert machine.interpret() == 6

    new_machine = Machine()
    pass_ = Pass(name="a_pass")
    new_machine.register(pass_)
    new_machine.register(task)

    input_ = Input(x=3)
    assert new_machine.interpret(input=input_) == 8


def test_compile_machine_with_single_task(registry):

    task = Task(
        name="add_with_defaults",
        resource="add_with_defaults",
        registry=registry
    )

    assert task.interpret() == 6

    machine = Machine()
    machine.register(task)
    
    compiled_expected = {
        "StartAt": "add_with_defaults",
        "States": {
            "add_with_defaults": {
                "Type": "Task",
                "Next": "End",
                "Resource": "add_with_defaults",
                "End": True
            }
        }
    }

    assert machine.compile() == compiled_expected


def test_compile_machine_with_task_and_transitions(registry):

    first_task = Task(
        name="add_two",
        resource="add_two",
        registry=registry
    )

    second_task = Task(
        name="add_with_defaults",
        resource="add_with_defaults",
        registry=registry
    )

    machine = Machine()
    machine.register(first_task)
    machine.register(second_task)

    compiled_expected = {
        "StartAt": "add_two",
        "States": {
            "add_two": {
                "Type": "Task",
                "Next": "add_with_defaults",
                "Resource": "add_two",
                "End": False
            },
            "add_with_defaults": {
                "Type": "Task",
                "Next": "End",
                "Resource": "add_with_defaults",
                "End": True
            }
        }
    }

    assert machine.compile() == compiled_expected
    
    

    

    
