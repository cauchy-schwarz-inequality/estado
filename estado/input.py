class Input:

    def __init__(self, **inputs):

        self.inputs = inputs

    def __repr__(self):

        inputs = "<Input:"
        for parameter in self.inputs:
            inputs += f"{parameter}:{self.inputs[parameter]}|"
            
        return inputs[:len(inputs)-1] + ">"
        
