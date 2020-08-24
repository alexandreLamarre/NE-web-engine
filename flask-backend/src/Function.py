import parser
from src.Error_Stack import ErrorStack
from sympy import *
from math import *
import os

SUPPORTED_MATH_FUNCTIONS = ["abs","log","cos", "sin", "tan","ceil", "ceiling","factorial","floor",\
                            "isqrt", "trunc", "pi", "e", "tau", "exp", "log2", "log10", "sqrt", "acos", "asin", "atan","atan2"\
                            "degrees", "radians", "acosh", "asinh", "atanh", "cosh", "sinh", "tanh", "erf", "erfc", "gamma", "lgamma"]

class Function(ErrorStack):
    def __init__(self, function_string):
        """
        (String) -> None

        Takes in a Function String preprocessed by the interpreter of FunctionManger
        Initializes the interface ErrorStack to push and return fatal compile time errors

        Initializes a set of attributes for:
                -user friendly output in the form of strings
                -A list of functions that can be evaluated at runtime
                -Information about the Domain and Co-Domain of the function
        """
        super().__init__()
        self.info_string = function_string
        self.name, self.str_vars, self.str_funcs = self._parse_input(function_string)
        ## process step: switch '^' to ** and multiply where necessary
        self.str_funcs = self.preprocess_function_string()
        self.funcs = self.create_funcs(self.str_funcs)
        self.in_dimension = len(self.str_vars)
        self.out_dimension = len(self.str_funcs)


    def _parse_input(self, function_matched_string):
        """
        (String) -> (String, String[], String[])

        Parses a string that meets the specification of the interpreter in FunctionManager
        Returns a String for the function name, a list of strings for the function variables, and
        a list of strings for the output functions
        """
        namevar_split_functions = function_matched_string.split("=")
        name_var = namevar_split_functions[0]

        function_set = namevar_split_functions[1]
        function_set = function_set.strip()
        function_set = function_set[1:-1]
        function_set = function_set.split(',')
        for i in range(len(function_set)):
            function_set[i] = function_set[i].strip()

        name_var = name_var.strip()
        name_var = name_var.split('(')

        name = name_var[0]
        name = name.strip()

        var = name_var[1]
        var = var.strip()
        var = var[:-1]
        var = var.split(",")
        for i in range(len(var)):
            var[i] = var[i].strip()
        return name, var, function_set

    def preprocess_function_string(self):
        ##TODO Doesn't account for variables of length >1
        for i in range(len(self.str_funcs)):
            self.str_funcs[i] = self.str_funcs[i].replace("^", "**")
            self.str_funcs[i] = self.str_funcs[i].replace(" ","")
            for var in self.str_vars:
                start_index= 0
                while var in self.str_funcs[i][start_index:]:
                    search_index = self.str_funcs[i].index(var,start_index)
                    start_index = search_index + 1
                    if not(start_index-2)<0:
                        ##check characters to the left of var
                        if self.str_funcs[i][search_index-1].isdigit() or self.str_funcs[i][search_index-1].isalpha() or self.str_funcs[i][search_index-1] == ")":
                            self.str_funcs[i] = self.str_funcs[i][:search_index] +"*"+self.str_funcs[i][search_index:]
                            start_index+=1
                    if not(start_index+len(var)-1)>len(self.str_funcs[i])-1:
                        if self.str_funcs[i][start_index+len(var)-1].isdigit() or self.str_funcs[i][start_index+len(var)-1].isalpha() or self.str_funcs[i][start_index+len(var)-1] == "(":
                            self.str_funcs[i] = self.str_funcs[i][:start_index+len(var)-1] + "*" + self.str_funcs[i][start_index+len(var)-1:]
                            start_index += 1
            start_index = 0
            while ")(" in self.str_funcs[i][start_index:]:
                search_index = self.str_funcs[i].index(")(",start_index)
                start_index = search_index + 1
                self.str_funcs[i] = self.str_funcs[i][:start_index] + "*" + self.str_funcs[i][start_index:]


            for j in range(len(SUPPORTED_MATH_FUNCTIONS)):
                start_index = 0
                if not SUPPORTED_MATH_FUNCTIONS[j] in self.str_vars:
                    while SUPPORTED_MATH_FUNCTIONS[j] in self.str_funcs[i][start_index:]:

                        search_index = self.str_funcs[i].index(SUPPORTED_MATH_FUNCTIONS[j], start_index)
                        start_index = search_index
                        if(start_index - 1) > 0:
                            if self.str_funcs[i][start_index-1].isdigit() or self.str_funcs[i][start_index-1].isalpha() or self.str_funcs[i][start_index-1] == ")":
                                self.str_funcs[i] = self.str_funcs[i][:start_index] +"*"+ self.str_funcs[i][start_index:]
                        start_index+=1

        return self.str_funcs

    def create_compiled_code(self, str_funcs):
        """
        (String[]) -> (python compilable code[])

        Compiles the output function strings into python compilable code
        Includes the python math standard library, except for functions that require ','
        because ',' delimits outputfunctions

        Returns a list of the python compilable code of these function strings
        """

        code_list = []
        for f in str_funcs:
            try:
                #TODO pre-process functions with certain symbols and lack of multiplication
                f2 = f.replace("^", "**")
                code = parser.expr(f2).compile()
                code_list.append(code)
            except SyntaxError:
                # self.push_errors("Invalid function {}".format(f))
                self.push_error("'{}' :Oops! Your function was misinterpreted by the compiler. Try explicitly multiplying things or specifying what standard functions act on by using parentheses \n".format(f))
        return code_list

    def create_eval_functions(self, code_list):
        """
        (Python Compilable code[]) -> (python functions [])

        Creates callable python functions by the passed in compilable code
        Makes sure the custom string variables are instantiated
        for evaluation in the module using 'exec' built in function
        Returns a list of python functions that can be executed and called
        """
        function_list = []
        for j in range(len(code_list)):
            def make_func(j):
                def f(vars, *args):
                    """
                    (Vars)x (value1, value2, ...) -> (float)
                    """
                    assert(len(vars) == len(args))
                    for i in range(len(vars)):
                        exec_str = "{}={}".format(vars[i], args[i])
                        exec(exec_str)
                    return eval(code_list[j])
                return f

            function_list.append(make_func(j))

        return function_list

    def create_funcs(self, str_funcs):
        """
        (String[]) -> (functions [])

        Helper function to compile python executable function and
        return their function definitions
        """
        code_list = self.create_compiled_code(str_funcs)
        return self.create_eval_functions(code_list)

    def evaluate(self, *args):
        """
        (int[]) or (float[]) -> (int[]) or (float[])

        Evaluates the function in Function object at *args
        Pushes appropriate errors
        """
        res = []
        for i in range(len(self.funcs)):
            try:
                value = self.funcs[i](self.str_vars, *args)
                res.append(value)
            except:
                res.append(None)

        return res

    def get_codomain_functions(self):
        """
        None -> (functions)

        Getter for functions of a Function object
        """
        return self.funcs

    def get_vars(self):
        """
        None -> (String[])

        Getter for variables of a Function object
        """
        return self.str_vars

    def get_latex(self):
        output_vars = ""
        for v in self.str_vars:
            output_vars += v + ","
            exec("{} = symbols('{}')".format(v, v))
        if len(output_vars)>1:
            output_vars = output_vars[:-1]
        output_funcs = ""
        for f in self.str_funcs:
            func = eval(f)
            output_funcs += latex(func) + ","

        if len(output_funcs) > 1:
            output_funcs = output_funcs[:-1]

        return self.name + "("+output_vars+")"+" = "+"$(" + output_funcs +")$"

    def __repr__(self):
        """
        __repr__ method used for unittesting
        """
        output_str = ""
        var_to_str = ""
        for v in self.str_vars:
            var_to_str += v + ','
        var_to_str = var_to_str[:-1]

        func_to_str = ""
        for f in self.str_funcs:
            func_to_str += f + ','
        func_to_str = func_to_str[:-1]
        output_str = "NAME: {} VARS: [{}] FUNCS [{}]".format(self.name, var_to_str, func_to_str)

        return output_str

if __name__ == "__main__":
    start_time = os.times()[0]
    i= 0
    function = Function("f(x) = (sin(2x),cos(x5))")
    i+=1
    function = Function("f(x,y) = (sin(2xy5), xlog(2x))")
    i+=1
    function = Function("f(cat) = (cat^2floor(cat))")
    i+=1
    function = Function("f(x,a) = (log(x)a)")
    print(function)
    end_time = os.times()[0]
    print("Completed {} tests in {} seconds".format(i,end_time - start_time))