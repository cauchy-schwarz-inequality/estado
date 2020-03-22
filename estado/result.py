class Result:

    def __init__(self, result=None, path="$.result", **results):

        self.path = path
        self.results = results
        
        if result or not results:
            self.results["result"] = result

    def compile(self):

        return self.results

    def __eq__(self, other):
        
        if isinstance(other, Result):
            return self.results == other.results

        elif isinstance(other, dict):
            return self.results == other

        elif (not hasattr(other, '__len__') and
              len(self.results) == 1):
            return (list(self.results.values())[0] ==
                    other)
        else:
            return False


    def __bool__(self):
        return bool(self.results)                    
            

    def __repr__(self):

        results = "<Result:"
        for result_parameter in self.results:
            results += f"{result_parameter}:{self.results[result_parameter]}|"
            
        return results[:len(results)-1] + ">"
        

        
