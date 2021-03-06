from src.OutputQueue import OutputQueue
from src.Error_Stack import ErrorStack
import parser
from sympy import *
from sympy.calculus.util import continuous_domain
from sympy.calculus.util import function_range
from src.FunctionManager import FunctionManager
import io
import os
import matplotlib.pyplot as plt
import base64
import matplotlib
matplotlib.use("Agg")

class Calculus(OutputQueue, ErrorStack):
    def __init__(self, functionManager):
        OutputQueue().__init__()
        ErrorStack().__init__()
        self.function_manager = functionManager
        self.Functions = [f for f in functionManager.Functions_container]
        self.jacobian = []

    def convert_latex_to_base64(self,latex):
        plt.close("all")
        buf = io.BytesIO()
        fig= plt.figure(figsize=(6.5,0.3))
        plt.rc('text')
        plt.axis('off')
        plt.text(0,0.3, f'${latex}$', size = 10)
        plt.savefig(buf, format = "png")
        plt.close("all")

        base64_string = base64.b64encode(buf.getvalue())
        return str(base64_string)

    def domain(self):
        output_list = []
        eval_list = []
        for f in self.Functions:
            code_list = []
            for var in f.str_vars:
                exec("{} = symbols('{}')".format(var, var))
            for function in f.str_funcs:
                for var in f.str_vars:
                    code = parser.expr("continuous_domain({},{},S.Reals)".format(function, var)).compile()
                    code_list.append(code)
            eval_list.append(code_list)
        for i in range(len(self.Functions)):
            for j in range(len(self.Functions[i].str_funcs)):
                output_list.append((self.Functions[i].str_funcs[j], latex(eval(eval_list[i][j]))))

        return output_list
    def range(self):
        output_list = []
        eval_list = []
        for f in self.Functions:
            code_list = []
            for var in f.str_vars:
                exec("{} = symbols('{}')".format(var, var))
            for function in f.str_funcs:
                for var in f.str_vars:
                    code = parser.expr("function_range({},{},S.Reals)".format(function, var)).compile()
                    code_list.append(code)
            eval_list.append(code_list)
        for i in range(len(self.Functions)):
            for j in range(len(self.Functions[i].str_funcs)):
                output_list.append(
                    (self.Functions[i].str_funcs[j], latex(eval(eval_list[i][j]))))

        return output_list

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
                var_root_tuple = (self.Functions[i].str_vars[j%roots_modulus],self.convert_latex_to_base64(latex(eval(eval_list[i][j])))[2:-1] )
                function_root_list.append(var_root_tuple)
            ##has only one range function and one variable
            if function_root_list != []:
                range_function_var_root_tuple = (
                self.Functions[i].str_funcs[(len(self.Functions[i].str_funcs) - 1) // roots_modulus], function_root_list)
                all_range_functions_root_list.append(range_function_var_root_tuple)
                function_root_list = []
            # if(all_range_functions_root_list == []):
            #     range_function_var_root_tuple = (
            #     self.Functions[i].str_funcs[0], function_root_list)
            #     all_range_functions_root_list.append(range_function_var_root_tuple)
            function_root_tuple = (self.Functions[i].info_string, all_range_functions_root_list)
            output_list.append(function_root_tuple)
        return output_list



    def derivative(self):
        ## should be a matrix of size rows = num range functions
        ##                         columns = num vars
        if not self.jacobian: #partial derivatives have not been calculated
            pass
        else:
            ##process self.jacobian into a latex matrix:
            pass
        return self.jacobian

    def integral(self):
        pass



    def partial_derivatives(self):
        ## Compile code for computing derivatives
        jacobian_list= []
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
                eval_expr = latex(eval(eval_list[i][j]))
                jacobian_list.append(eval_expr)
                var_root_tuple = (self.Functions[i].str_vars[j % roots_modulus], self.convert_latex_to_base64(eval_expr)[2:-1])
                function_root_list.append(var_root_tuple)
            ##has only one range function and one variable
            if function_root_list != []:
                range_function_var_root_tuple = (
                self.Functions[i].str_funcs[(len(self.Functions[i].str_funcs) - 1) // roots_modulus], function_root_list)
                all_range_functions_root_list.append(range_function_var_root_tuple)
                function_root_list = []
            # if (all_range_functions_root_list == []):
            #     range_function_var_root_tuple = (
            #         self.Functions[i].str_funcs[0], function_root_list)
            #     all_range_functions_root_list.append(range_function_var_root_tuple)
            function_root_tuple = (self.Functions[i].info_string, all_range_functions_root_list)
            output_list.append(function_root_tuple)
        self.jacobian = jacobian_list
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
                var_root_tuple = (self.Functions[i].str_vars[j % roots_modulus], self.convert_latex_to_base64(latex(eval(eval_list[i][j])))[2:-1])
                function_root_list.append(var_root_tuple)
            ##has only one range function and one variable
            if function_root_list != []:
                range_function_var_root_tuple = (
                self.Functions[i].str_funcs[(len(self.Functions[i].str_funcs) - 1) // roots_modulus], function_root_list)
                all_range_functions_root_list.append(range_function_var_root_tuple)
                function_root_list = []
            # if (all_range_functions_root_list == []):
            #     range_function_var_root_tuple = (
            #         self.Functions[i].str_funcs[0], function_root_list)
            #     all_range_functions_root_list.append(range_function_var_root_tuple)
            function_root_tuple = (self.Functions[i].info_string, all_range_functions_root_list)
            output_list.append(function_root_tuple)
        return output_list

if __name__ == "__main__":
    fm = FunctionManager("f(x,y) = (log(x+y),y)")
    calc = Calculus(fm)
    print(calc.range())
    # start_time = os.times()[0]
    # funct = FunctionManager("f(x,y) = (cos(x+y))")
    # calcs = Calculus(funct)
    # zeros = calcs.zeroes()
    # print(zeros)
    #
    #
    # derivatives = calcs.partial_derivatives()
    # print(derivatives)
    #
    #
    #
    # integrals = calcs.partial_integrals()
    # print(integrals)
    # end_time = os.times()[0]
    # print("Finished in {} seconds".format(end_time-start_time))
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
