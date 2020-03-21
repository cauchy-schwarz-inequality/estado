from estado.machine import Machine


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
