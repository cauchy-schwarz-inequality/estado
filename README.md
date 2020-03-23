# Estado 

Estado is a language for describing state machines. 

## Example interaction

Supposing a state machine consisting of two pass states, initialized as follows:

``` python
from estado.pass_state import Pass
machine = Pass(name="FirstPass") + Pass(name="SecondPass")
```
Note that this is equivalent to the following 

``` python
from estado.input import Input
from estado.machine import Machine
from estado.pass_state import Pass

machine = Machine()
machine.register(Pass(name="FirstPass"))
machine.register(Pass(name="SecondPass"))
```

We can compile it to valid Amazon States Language with

``` python
machine.compile()
```
which returns 

``` json
{
  "StartAt": "FirstPass",
  "States": {
    "FirstPass": {
      "Type": "Pass",
      "Next": "SecondPass",
      "End": false
    },
    "SecondPass": {
      "Type": "Pass",
      "End": true
    }
  }
}
```
We can interpret the machine with an initial input:

``` python
x = Input(x=5)
machine.interpret(input=x)
```
which returns the Estado representation `<Input:input:5>`. 

## Task states

There is support for interpreting task states. We can use the `estado.resource_registry.Registry` class to register function resources.

Given a registry initialized with a function:

``` python
from estado.resource_registry import Registry

registry = Registry()
add_two = lambda x: x + 2
registry.register_function(add_two, "add_two")
```

We can interpret a simple machine as follows:

``` python
from estado.input import Input
from estado.task_state import Task

first_state = Pass(
        name="state_one"
)
second_state = Task(
        name="AddTwo",
        resource="add_two",
        registry=registry
)

machine = first_state + second_state
machine.interpret(input=Input(x=5))
```

which returns `<Result:result:7>`, with compilation via the `compile` method outputting

``` json
{
  "StartAt": "state_one",
  "States": {
    "state_one": {
      "Type": "Pass",
      "Next": "add_two",
      "End": false
    },
    "AddTwo": {
      "Type": "Task",
      "End": true,
      "Resource": "registry:add_two"
    }
  }
}
```

## Tests 

To run the tests, ensure you have `pytest` on your path. Then do `pytest` from the project root. 
