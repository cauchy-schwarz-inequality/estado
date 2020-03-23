from estado.hash_utils import slug_hash

class Registry:

    def __init__(self):
        self.functions = {}

    def register_function(self, fn, name=""):

        if not name:
            name = slug_hash()

        self.functions[name] = fn


    def invoke_function(self, name, **kwargs):

        fn = self.functions[name]

        return fn(**kwargs)


class RegistryException(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)

        
