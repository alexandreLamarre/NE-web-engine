from src.interpreter import FunctionInterpreter
from src.Error_Stack import ErrorStack
from src.Function import Function

class FunctionManager(FunctionInterpreter):
    """Factory object that processes the input arguments inside a command object
    Instantiates these inputs into custom Function objects

    Implements an Interpreter interface because it processes input in the command"""
    def __init__(self, function_strs):
        """
        (String) -> None

        Initializes a Function Manager with a list of Functions and user friendly strings with getters
        """
        super().__init__()
        self.Functions_str_container = self.match(function_strs)
        self.uninterpreted = self.process_uninterpreted(function_strs)

        self.Functions_container = [Function(f) for f in self.Functions_str_container]

    def process_uninterpreted(self, in_str):
        """
        (String) -> (String)

        Processes uninterpreted input in the command arguments by removing the interpreted input
        and separating them.

        Returns a user friendly string.
        """
        res = in_str
        for fstr in self.Functions_str_container:
            assert(fstr in res), "Interpreted input was not even in the input to begin with??"
            start_index = res.find(fstr)
            end_index = start_index+len(fstr)
            res = res[0:start_index].strip() +"\n"+ res[end_index:].strip()
            res.strip()
        return res

    def get_uninterpreted(self):
        """
        None -> (String)

        Returns a user friendly string that indicates which input is uninterpreted by the FunctionManager
        """
        output = self.uninterpreted.strip()

        return "The following could not be interpreted as a function :" + output if output else ""

    def get_interpreted(self):
        """
        None -> (String)

        Returns a user friendly string that indicates which input is interpreted by the FunctionManager
        """
        res = ''
        for f in self.Functions_str_container:
            res += f
            res += ' '
        res = res.strip()
        return "Functions:" + " " +res if res else ""

    def get_compile_errors(self):
        """
        None -> (String)

        Checks the container of Function objects to see if they encountered any
        fatal errors compiling or evaluating their user-interpreted functions.
        """
        errors = ""
        for f in self.Functions_container:
            input_values = [0]*f.in_dimension
            f.evaluate(*input_values)
            errors += f.check_errors()
        return errors

    def generate_uninterpreted_reason(self):
        """
        #TODO
        """
        pass

if __name__ == "__main__":
    test = FunctionManager("laplace(x,y,z) = (x, y**(1/3), z**(1/3)) fourrier(x) = (x//y)}")
    print(test.get_compile_errors())