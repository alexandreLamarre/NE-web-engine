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
        self.ErrorStack = ErrorStack()
        self.Functions_str_container = self.process_functions(function_strs)
        self.uninterpreted = self.process_uninterpreted(function_strs)

        self.Functions_container = [Function(f) for f in self.Functions_str_container]

    def process_functions(self,function_string):
        output_strings = self.match(function_string)
        return output_strings

    def generate_reason_uninterpreted(self, uninterpreted_string):
        balanced_parentheses = 0
        for el in uninterpreted_string:
            if el == "(":
                balanced_parentheses += 1
            if el == ")":
                balanced_parentheses -= 1
        if balanced_parentheses != 0:
            self.ErrorStack.push_error("Mismatched parantheses in '{}'  ".format(uninterpreted_string))
        if "=" not in uninterpreted_string and uninterpreted_string.strip() != "":
            self.ErrorStack.push_error("'{}' : Function declarations must contain an equal sign  ".format(uninterpreted_string))

        var_errors = self.partial_match_variables(uninterpreted_string)
        if var_errors:
            for e in var_errors:
                self.ErrorStack.push_error("Invalid variables declaration in '{}'  ".format(e))
        var_errors = self.partial_match_name(uninterpreted_string)
        if var_errors:
            for e in var_errors:
                self.ErrorStack.push_error("Invalid function name declaration in '{}'  ".format(e))
        var_errors = self.partial_match_function(uninterpreted_string)
        if var_errors:
            for e in var_errors:
                self.ErrorStack.push_error("Invalid output function definition in '{}'  ".format(e))
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
        self.generate_reason_uninterpreted(res)
        return res

    # def get_uninterpreted(self):
    #     """
    #     None -> (String)
    #
    #     Returns a user friendly string that indicates which input is uninterpreted by the FunctionManager
    #     """
    #     output = self.uninterpreted.strip()
    #
    #     return "The following could not be interpreted as a function :" + output if output else ""

    def get_interpreted(self):
        """
        None -> (String)

        Returns a user friendly string that indicates which input is interpreted by the FunctionManager
        """
        res = ''
        for f in self.Functions_container:
            res += f.info_string
            res += ' '
        res = res.strip()
        return res if res else ""

    def get_errors(self):
        output_str = ""
        output_str += self.ErrorStack.get_errors()
        for f in self.Functions_container:
            output_str += f.get_errors() + " "
        return output_str[:-1] if len(output_str)>1 else ""
    # def get_compile_errors(self):
    #     """
    #     None -> (String)
    #
    #     Checks the container of Function objects to see if they encountered any
    #     fatal errors compiling or evaluating their user-interpreted functions.
    #     """
    #     errors = ""
    #     for f in self.Functions_container:
    #         input_values = [0]*f.in_dimension
    #         f.evaluate(*input_values)
    #         errors += f.check_errors()
    #     return errors

    def generate_uninterpreted_reason(self):
        """
        #TODO
        """
        pass

if __name__ == "__main__":
    test = FunctionManager("f(x) = (cos(x),sin(x)")
    print(test.Functions_str_container)