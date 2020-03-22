from estado.state import State
from estado.hash_utils import slug_hash

class Pass(State):

    JSON_ = {
        "Type": "Pass",
        "Next": "End"
    }

    def __init__(self, input=None,
                 result=None, name="",
                 next=None, end=False):
        State.__init__(self, next, result, end)

        if not name:
            self.name = slug_hash()

        self.input = input
        self.result = result

    def run(self):

        if not self.result:
            return self.input

        return self.result
