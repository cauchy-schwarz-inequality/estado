from estado.machine import Machine
from estado.pass_state import Pass


def test_toplevel():
    """
    A State Machine MUST have an object field named “States”, whose fields represent the states.

    A State Machine MUST have a string field named “StartAt”, whose value MUST exactly match one of names of the “States” fields. 
    The interpreter starts running the the machine at the named state.
    """
    
    machine = Machine()
    compiled = machine.compile()
    
    assert "States" in compiled
    assert "StartAt" in compiled

def test_pass_state_empty():
    """
    The Pass State (identified by "Type":"Pass") simply passes its input to its output, performing no work. 

    A Pass State MAY have a field named “Result”. 

    If present, its value is treated as the output of a virtual task, and placed as prescribed by the “ResultPath” field, 
    if any, to be passed on to the next state. 

    If “Result” is not provided, the output is the input. 

    Thus if neither “Result” nor “ResultPath” are provided, the Pass state copies its input through to its output.
    """
    
    machine = Machine()
    pass_ = Pass()
    machine.register(pass_)
    pass_run_result = machine.run()

    assert pass_run_result is None

    

def test_pass_state_nonempty():
    machine = Machine()
    pass_ = Pass(2)
    machine.register(pass_)
    pass_run_result = machine.run()

    assert pass_run_result == 2

    pass_ = Pass(result=5)
    machine_2 = Machine()
    machine_2.register(pass_)
    pass_2_run_result = machine_2.run()

    assert pass_2_run_result == 5
    
    

    # machine_two = Machine()
    # pass_two = Pass(2)
    # machine.register(pass_two)
    # pass_two_run_result = machine.run()

    # assert pass_two_run_result == 2
    
    
    
    
