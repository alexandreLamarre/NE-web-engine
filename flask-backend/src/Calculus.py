from src.OutputQueue import OutputQueue
from src.Error_Stack import ErrorStack
import parser
from sympy import *
from src.FunctionManager import FunctionManager
from io import BytesIO
from PIL import Image, ImageTk
import os

class Calculus(OutputQueue, ErrorStack):
    def __init__(self, functionManager):
        OutputQueue().__init__()
        ErrorStack().__init__()
        self.function_manager = functionManager
        self.Functions = [f for f in functionManager.Functions_container]

    def symbolize(self):
        """
        #TODO
        Takes the string arguments for each function in Function Manger and returns
        displayable? symbolic functions that can be turned into latex????
        """
        ### Actually no idea if this is the right way to do this, should look at sympy documentation
        output_list = []
        for f in self.Functions:
            code_list = []
            for var in f.str_vars:
                exec("{} = symbols('{}')".format(var,var))
            for function in f.str_funcs:
                code = parser.expr("{}".format(function)).compile()
                code_list.append(code)
            output_list.append(code_list)
        return output_list

    def zeroes(self):
        """ Computes symbolic zeroes of the functions passed in
        Returns nested list of lists where the i-th
        nested list is the set of roots of the ith function"""

        ## Compile code for computing zerores
        eval_list = []
        for f in self.Functions:
            code_list = []
            for var in f.str_vars:
                exec("{} = symbols('{}')".format(var, var))
            for function in f.str_funcs:
                for var in f.str_vars:
                    code = parser.expr("solveset({}, {})".format(function, var)).compile()
                    code_list.append(code)
            eval_list.append(code_list)

        ## Eval code for computing zeroes
        output_list = []
        for i in range(len(self.Functions)):
            function_root_list = []
            all_range_functions_root_list = []
            roots_modulus = len(self.Functions[i].str_vars)
            for j in range(len(eval_list[i])):
                if j%roots_modulus == 0 and j != 0:
                    range_function_var_root_tuple = (self.Functions[i].str_funcs[(j-1)//roots_modulus], function_root_list)
                    all_range_functions_root_list.append(range_function_var_root_tuple)
                    function_root_list = []
                var_root_tuple = (self.Functions[i].str_vars[j%roots_modulus],latex(eval(eval_list[i][j])))
                function_root_list.append(var_root_tuple)
            ##has only one range function and one variable
            if(all_range_functions_root_list == []):
                range_function_var_root_tuple = (
                self.Functions[i].str_funcs[0], function_root_list)
                all_range_functions_root_list.append(range_function_var_root_tuple)
            function_root_tuple = (self.Functions[i].info_string, all_range_functions_root_list)
            output_list.append(function_root_tuple)
        return output_list



    def derivative(self):
        ## should be a matrix of size rows = num range functions
        ##                         columns = num vars
        pass

    def integral(self):
        pass



    def partial_derivatives(self):
        ## Compile code for computing derivatives
        eval_list = []
        for f in self.Functions:
            code_list = []
            for var in f.str_vars:
                exec("{} = symbols('{}')".format(var, var))
            for function in f.str_funcs:
                for var in f.str_vars:
                    code = parser.expr("diff({}, {})".format(function, var)).compile()
                    code_list.append(code)
            eval_list.append(code_list)

        output_list = []
        for i in range(len(self.Functions)):
            function_root_list = []
            all_range_functions_root_list = []
            roots_modulus = len(self.Functions[i].str_vars)
            for j in range(len(eval_list[i])):
                if j % roots_modulus == 0 and j != 0:
                    range_function_var_root_tuple = (
                        self.Functions[i].str_funcs[(j - 1) // roots_modulus], function_root_list)
                    all_range_functions_root_list.append(range_function_var_root_tuple)
                    function_root_list = []
                var_root_tuple = (self.Functions[i].str_vars[j % roots_modulus], latex(eval(eval_list[i][j])))
                function_root_list.append(var_root_tuple)
            ##has only one range function and one variable
            if (all_range_functions_root_list == []):
                range_function_var_root_tuple = (
                    self.Functions[i].str_funcs[0], function_root_list)
                all_range_functions_root_list.append(range_function_var_root_tuple)
            function_root_tuple = (self.Functions[i].info_string, all_range_functions_root_list)
            output_list.append(function_root_tuple)
        return output_list

    def second_order_partials(self):
        pass

    def specific_partials(self, partial_list):
        pass

    def partial_integrals(self):
        eval_list = []
        for f in self.Functions:
            code_list = []
            for var in f.str_vars:
                exec("{} = symbols('{}')".format(var, var))
            for function in f.str_funcs:
                for var in f.str_vars:
                    code = parser.expr("integrate({}, {})".format(function, var)).compile()
                    code_list.append(code)
            eval_list.append(code_list)

        output_list = []
        for i in range(len(self.Functions)):
            function_root_list = []
            all_range_functions_root_list = []
            roots_modulus = len(self.Functions[i].str_vars)
            for j in range(len(eval_list[i])):
                if j % roots_modulus == 0 and j != 0:
                    range_function_var_root_tuple = (
                        self.Functions[i].str_funcs[(j - 1) // roots_modulus], function_root_list)
                    all_range_functions_root_list.append(range_function_var_root_tuple)
                    function_root_list = []
                var_root_tuple = (self.Functions[i].str_vars[j % roots_modulus], latex(eval(eval_list[i][j])))
                function_root_list.append(var_root_tuple)
            ##has only one range function and one variable
            if (all_range_functions_root_list == []):
                range_function_var_root_tuple = (
                    self.Functions[i].str_funcs[0], function_root_list)
                all_range_functions_root_list.append(range_function_var_root_tuple)
            function_root_tuple = (self.Functions[i].info_string, all_range_functions_root_list)
            output_list.append(function_root_tuple)
        return output_list

if __name__ == "__main__":
    start_time = os.times()[0]
    funct = FunctionManager("f(x,y) = (x**2-1 , x+y, y**2+3) g(x) = (x**3)")
    calcs = Calculus(funct)
    zeros = calcs.zeroes()

    print(zeros)
    str_output = str(zeros[0][0])
    print(str_output)

    derivatives = calcs.partial_derivatives()
    print(derivatives)



    integrals = calcs.partial_integrals()
    print(integrals)
    end_time = os.times()[0]
    print("Finished in {} seconds".format(end_time-start_time))
    # expr = "\mathbb{R}"
    # expr = expr + "$\displaystyle" + expr + "$"
    # f = BytesIO()
    # preview(expr,viewer = "BytesIO", output = "ps",preamble = r"\documentclass{standalone}"
    #                r"\usepackage{pagecolor}"
    #                r"\begin{document}"
    #                r"\setmainfont{Times New Roman}", outputbuffer=f)
    # f.seek(0)
    #
    # img = Image.open(f)
    # img.load(scale = 10)
    # img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), Image.BILINEAR)
    # f.close()