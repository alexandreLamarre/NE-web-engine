import parser
from src.Error_Stack import ErrorStack
from sympy import *
from math import *
import os
import re

SUPPORTED_MATH_FUNCTIONS = ["abs","log","cos", "sin", "tan","ceil", "ceiling","factorial","floor",\
                            "isqrt", "trunc", "exp", "log2", "log10", "sqrt", "acos", "asin", "atan",\
                            "degrees", "radians", "acosh", "asinh", "atanh", "cosh", "sinh", "tanh", "erf", "erfc", "gamma", "lgamma"]

SUPPORTED_MATH_CONSTANTS = ["pi","tau", "e"]
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
        self.name, self.str_vars, self.str_funcs = self._parse_input(function_string)
        self.str_vars = self.preprocess_variables()
        ## process step: switch '^' to ** and multiply where necessary
        self.str_funcs = self.preprocess_function_string()
        self.info_string = self.generate_interpreted()
        self.funcs = self.create_funcs(self.str_funcs)
        self.in_dimension = len(self.str_vars)
        self.out_dimension = len(self.str_funcs)
        ## Test evaluation
        test_list = [0] *len(self.str_vars)
        self.evaluate(*test_list)



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
        ##remove 'empty' functions
        while "" in function_set:
            function_set.remove("")

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

    def generate_interpreted(self):
        res = ''
        res += self.name
        res += "("
        for var in self.str_vars:
            res += var + ","
        res = res[:-1] if res[-1] != "(" else res
        res += ") = ("
        for func in self.str_funcs:
            res += func + ","
        res = res[:-1] if res[-1] != "(" else res
        res += ")"
        return res

    def preprocess_variables(self):
        cur_vars = self.str_vars
        ## we don't use list(set(cur_vars)) because we want to preserve user input order
        distinct_vars = []
        for v in cur_vars:
            if v not in distinct_vars:
                distinct_vars.append(v)
        return distinct_vars

    def order_vars(self):
        """Return variables but ordered in terms of decreasing length"""
        cur_vars = list(self.str_vars) ## create a copy to preserve user given input order in the output

        return sorted(cur_vars, key=len, reverse = True)

    def allowed_chars(self, var, ordered_var):
        """
        Assumption: no repeated variables (guaranteed by preprocess variables)
        """
        allowed_left_chars = []
        allowed_right_chars = []
        if var in ordered_var:  # if call this we checking variables
            search = ordered_var[:ordered_var.index(var)]

        else:   ## if we call this with builtin functions or builtin-constants
            search = ordered_var
        for v in search:
            if var in v:
                left_index = v.index(var)
                right_index = v.rfind(var)+len(var)
                if(left_index - 1) >= 0:
                    allowed_left_chars.append(v[left_index-1])
                if(right_index < len(v)):
                    allowed_right_chars.append(v[right_index])
        for j in SUPPORTED_MATH_FUNCTIONS:
            if var in j:
                left_index = j.index(var)
                right_index = j.rfind(var) + len(var)
                if left_index-1 >= 0:
                    allowed_left_chars.append(j[left_index-1])
                if(right_index < len(j)):
                    allowed_right_chars.append(j[right_index])
                else:
                    allowed_right_chars.append(j)
        return allowed_left_chars,allowed_right_chars

    def preprocess_parantheses(self, cur_func):
        start_index = 0
        while ")(" in cur_func[start_index:]:
            search_index = cur_func.index(")(", start_index)
            start_index = search_index + 1
            cur_func = cur_func[:start_index] + "*" + cur_func[start_index:]
        j = 0
        length = len(cur_func)
        while(j<length):
            if cur_func[j] == ")":
                if j + 1< len(cur_func) and cur_func[j+1].isdigit():
                    cur_func = cur_func[:j+1] + "*" +cur_func[j+1:]
                    length += 1
            if(cur_func[j] == "("):
                if j - 1 >= 0 and cur_func[j-1].isdigit():
                    if j - len("log10") >= 0:
                        if cur_func[j-len("log10"):j] != "log10":
                            cur_func = cur_func[:j] + "*" + cur_func[j:]
                            length += 1
                    elif j - len("log2") >= 0:
                        if cur_func[j-len("log2"):j] != "log2":
                            cur_func = cur_func[:j] + "*" + cur_func[j:]
                            length += 1
                    else:
                        cur_func = cur_func[:j] + "*" + cur_func[j:]
                        length += 1

            j += 1
        return cur_func

    def preprocess_functions_variables(self,cur_func):
        ordered_vars = self.order_vars()
        for var in ordered_vars:
            start_index = 0
            allowed_left, allowed_right = self.allowed_chars(var,ordered_vars)
            while var in cur_func[start_index:]:
                search_index = cur_func.index(var, start_index)
                start_index = search_index + 1
                if not (start_index - 2) < 0:
                    ##check characters to the left of var
                    if cur_func[search_index - 1].isdigit():
                        cur_func = cur_func[:search_index] + "*" + cur_func[search_index:]
                        start_index += 1
                    if cur_func[search_index - 1].isalpha() and (cur_func[search_index-1] not in allowed_left):
                        cur_func = cur_func[:search_index] + "*" + cur_func[search_index:]
                        start_index += 1
                    if  cur_func[search_index - 1] == ")":
                        cur_func = cur_func[:search_index] + "*" + cur_func[search_index:]
                        start_index += 1
                pivot = start_index + len(var) - 1
                if not (pivot) > len(cur_func) - 1:
                    ## check characters to the right of var
                    if cur_func[pivot].isdigit():
                        cur_func = cur_func[:pivot] + "*" + cur_func[pivot:]
                        start_index += 1
                    if cur_func[pivot].isalpha() and (cur_func[pivot] not in allowed_right):
                        cur_func = cur_func[:pivot] + "*" + cur_func[pivot:]
                        start_index += 1
                    if cur_func[start_index + len(var) - 1] == "(":
                        if(start_index-2 >=0):
                            if(cur_func[start_index-2] not in allowed_left):
                                cur_func = cur_func[:pivot] + "*" + cur_func[pivot:]
                                start_index += 1
                        else:
                            cur_func = cur_func[:pivot] + "*" + cur_func[pivot:]
                            start_index += 1
        return cur_func

    def preprocess_builtin_functions(self, cur_func):
        for j in range(len(SUPPORTED_MATH_FUNCTIONS)):
            start_index = 0
            if not SUPPORTED_MATH_FUNCTIONS[j] in self.str_vars:
                allowed_left, allowed_right = self.allowed_chars(SUPPORTED_MATH_FUNCTIONS[j], list(self.str_vars))
                # if SUPPORTED_MATH_FUNCTIONS[j] == "cos" or SUPPORTED_MATH_FUNCTIONS[j] == "sin":
                #     print(allowed_left)
                while SUPPORTED_MATH_FUNCTIONS[j] in cur_func[start_index:]:
                    search_index = cur_func.index(SUPPORTED_MATH_FUNCTIONS[j], start_index)
                    start_index = search_index + 1
                    if (start_index - 2) >= 0:
                        if cur_func[start_index - 2].isdigit():
                            cur_func = cur_func[:start_index-1] + "*" + cur_func[start_index-1:]
                            start_index += 1
                        if cur_func[start_index - 2] == ")":
                            cur_func = cur_func[:start_index-1] + "*" + cur_func[start_index-1:]
                            start_index += 1
                        if cur_func[start_index - 2].isalpha():
                            builtin = SUPPORTED_MATH_FUNCTIONS[j]
                            if builtin == "cos" or builtin == "sin" or builtin == "tan":
                                allowed_left.append("a")
                            if cur_func[start_index - 2] not in allowed_left:
                                # if (SUPPORTED_MATH_FUNCTIONS[j] == "cos" or SUPPORTED_MATH_FUNCTIONS[j] == "sin" or SUPPORTED_MATH_FUNCTIONS[j] == "tan"):
                                #     if(cur_func[start_index-2] != "a"):

                                cur_func = cur_func[:start_index-1] + "*" + cur_func[start_index-1:]
        return cur_func

    def preprocess_builtin_constants(self,cur_func):
        for k in range(len(SUPPORTED_MATH_CONSTANTS)):
            start_index = 0
            if not SUPPORTED_MATH_CONSTANTS[k] in self.str_vars:
                allowed_left, allowed_right = self.allowed_chars(SUPPORTED_MATH_CONSTANTS[k], list(self.str_vars))
                while (SUPPORTED_MATH_CONSTANTS[k]) in cur_func[start_index:]:
                    search_index = cur_func.index(SUPPORTED_MATH_CONSTANTS[k], start_index)
                    start_index = search_index + 1  # must increment by at least one every time or we can get stuck in an infinite loop
                    inserted_left = False
                    inserted_right = False
                    ##check characters to the left of known constants
                    if start_index - 2 >= 0:
                        if cur_func[start_index - 2].isdigit():
                            cur_func = cur_func[:start_index - 1] + "*" + cur_func[start_index - 1:]
                            inserted_left = True
                        if cur_func[start_index - 2].isalpha():
                            if cur_func[start_index - 2] not in allowed_left:
                                cur_func = cur_func[:start_index - 1] + "*" + cur_func[start_index - 1:]
                                inserted_left = True
                        if cur_func[start_index - 2] == ")":
                            cur_func = cur_func[:start_index - 1] + "*" + cur_func[start_index - 1:]
                            inserted_left = True
                    if inserted_left:
                        start_index += 1
                    ##check characters to the right of known constants
                    right_pivot = start_index + len(SUPPORTED_MATH_CONSTANTS[k]) -1
                    if right_pivot < len(cur_func):
                        if cur_func[right_pivot].isdigit():
                            cur_func = cur_func[:right_pivot] + "*" + cur_func[right_pivot:]
                            inserted_right = True
                        if cur_func[right_pivot] == "(":
                            cur_func = cur_func[:right_pivot] + "*" + cur_func[right_pivot:]
                            inserted_right = True
                        if cur_func[right_pivot].isalpha():
                            if cur_func[right_pivot] not in allowed_right:
                                cur_func = cur_func[:right_pivot] + "*" + cur_func[right_pivot:]
                                inserted_right = True
                        if inserted_right:
                            start_index += len(SUPPORTED_MATH_CONSTANTS[k])
        return cur_func

    def preprocess_function_string(self):

        output_funcs = []
        for i in range(len(self.str_funcs)):
            cur_func = self.str_funcs[i].replace("^", "**")
            cur_func = cur_func.replace(" ","")

            ##preprocess variables in functions
            cur_func = self.preprocess_functions_variables(cur_func)
            ##process parentheses in functions
            cur_func = self.preprocess_parantheses(cur_func)
            ##preprocess the functions provided by the math standard library
            cur_func = self.preprocess_builtin_functions(cur_func)
            ##preprocess the constants provided by the math standard library
            cur_func = self.preprocess_builtin_constants(cur_func)


            output_funcs.append(cur_func)
        return output_funcs

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
                self.push_error("'{}' :Oops! Your function was misinterpreted by the compiler. One or more variables/functions you are using may not be defined. \n".format(f))
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
            except ValueError:
                res.append(None)
            except NameError:
                self.push_error(self.generate_reason_uninterpreted())
            except TypeError:
                self.push_error("A standard function requires parentheses")
            except Exception as e:
                self.push_error(e)

        return res

    def generate_reason_uninterpreted(self):
        function_list_uninterpreted = []
        output_string = ""
        for i in range(len(self.str_funcs)):
            cur_func = self.str_funcs[i]
            cur_func = cur_func.replace("*", " ")
            cur_func = cur_func.replace("(", " ")
            cur_func = cur_func.replace(")", " ")
            cur_func = re.sub('\d', ' ', cur_func)

            for var in self.str_vars:
                cur_func = cur_func.replace(var, " ")
            math_functions_ordered = sorted(SUPPORTED_MATH_FUNCTIONS, key =len, reverse = True)
            for f in math_functions_ordered:
                cur_func = cur_func.replace(f, " ")
            for c in SUPPORTED_MATH_CONSTANTS:
                cur_func = cur_func.replace(c, " ")
            function_list_uninterpreted.append(cur_func)
        num_els = 0
        for f in function_list_uninterpreted:
            uninterpreted_element = f.split()
            for el in uninterpreted_element:
                output_string += "'{}', ".format(el)
                num_els += 1
        if output_string:
            output_string = output_string[:-2]

        intermediate = " are not a variable, common constant or common function" if num_els > 1 else " is not a variable, common constant or common function"
        return output_string + intermediate if output_string else ""

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
    function = Function("f(xax,xax) = (xaxxax)")
    print(function)
    print(function.get_errors())
    i+=1
    function = Function("f(x) = (sin(2x),cos(x5))")
    i+=1
    function = Function("f(x,y) = (sin(2xy5), xlog(2x))")
    i+=1
    function = Function("f(cat) = (cat^2floor(cat))")
    i+=1
    function = Function("f(x,a) = (log(x)a)")
    print(function)
    i += 1
    function = Function("f(x,a) = (pixa2pi3)")
    print(function)
    i += 1
    function = Function("f(piad,a) = (pi2piapipiad)")
    print(function)
    i+=1##checking for 'a' as var splits up 'piad' as a var
    function = Function("f(pied,a) = (pi2piapipied)")
    i += 1
    print(function) ## no idea whats wrong but pi*pi*ed should be pi*pied
    function = Function("f(pied, pie, pi, p) = (piedpiepip)")
    i += 1
    print(function)
    function = Function("f(randomcosvariable, randomsinvariable) = (randomcosvariablerandomsinvariable)")
    i += 1
    print(function)
    function = Function("f(x) = (cos(x)2acos(x)2)")
    i += 1
    print(function)

    function = Function("f(x) = (2(x+1))")
    i += 1
    print(function)
    function = Function("f(og) = (log(og))")
    i += 1
    print(function)
    function = Function("f(l)= (log(l))")
    i += 1
    print(function)
    function = Function("f(x,a) = (xacosh(x))")
    i += 1
    print(function)
    function = Function("f(x) = (eerf(x))")
    i += 1
    print(function)
    function = Function("f(x) = (lgamma(x))")
    i += 1
    print(function)
    function = Function("f(x) = (ceil(x))")
    i += 1
    print(function)
    function = Function("f(x) = (isqrt(x))")
    i += 1
    print(function)
    function = Function("f(ei) = (ceil(ei))")
    i += 1
    print(function)
    function = Function("f(ling) = (ceiling(ling))")
    i += 1
    function = Function("f(x,og) = (og(x))")
    print(function)
    end_time = os.times()[0]
    print("Completed {} tests in {} seconds".format(i,end_time - start_time))
