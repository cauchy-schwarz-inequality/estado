class Machine:

    TOPLEVEL = {
        "StartAt": "",
        "States": {
        }
    }

    def compile(self, force=False):

        if not force:
            self.validate()

        return self.TOPLEVEL

    def validate(self):
        pass
