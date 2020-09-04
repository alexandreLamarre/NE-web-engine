from src.FunctionManager import FunctionManager
from src.MarkovChainManager import MarkovChainManager
from src.Plot import Plot
from src.Calculus import Calculus
from src.MarkovChainManager import MarkovChainManager
from src.Error_Stack import ErrorStack

class Command():
    """
    Factory Object that manages the creation of DataManager Objects, i.e. FunctionManager

    Responsible for running one user command based on how it is initialized.
    Fetches error/interpreted/uninterpreted information from DataManager subclasses
    """
    def __init__(self, command_str):
        """
        None -> (String)

        Process inputs into command strings and argument strings
        Then uses a dictionary to match the argument to a known DataManager Object based on the command
        """
        # 'Static dictionary for the valid input classes inside the command given
        # In the future should be replaced by a database
        self.original_input = command_str
        self.ErrorStack = ErrorStack()
        self.commands_dict = {'plot': ['FunctionManager'], 'IFS': ['FunctionManager', 'MarkovChain'], \
                              'zeroes' : ['FunctionManager'], 'derivative': ['FunctionManager'], 'integral' : ['FunctionManager'],\
                              'partialderivative' : ['FunctionManager'], 'partialintegral': ['FunctionManager'], \
                              'chain': ["Chain"]}
        self.arguments = self.process_input(command_str)
        self.command = self.process_command(command_str)


        self.input_types = []

        if self.command in self.commands_dict:
            self.math_types = self.commands_dict[self.command]
            self.math_objects = self.process_input_types()
        else:
            self.math_types = []
            self.math_objects = []


    def run(self):
        """
        Runs the command specified on its arguments
        Should return the label of the widget it should be displayed in AND
        Should return the tuple (sublabels, info) that should be displayed in label should be displayed in
        """
        output = []
        all_errors = ""
        main_label = self.command
        if self.command == 'plot':
            for math in self.math_objects:
                if isinstance(math,FunctionManager):
                    plot = Plot(math)
                    figures, errors = plot.run()
                    all_errors += errors + "\n"
                    for f in figures:
                        output.append((None, f))
        if self.command == "zeroes":
            for math in self.math_objects:
                if isinstance(math, FunctionManager):
                    calc = Calculus(math)
                    zeroes = calc.zeroes()
                    for z in zeroes:
                        output.append((z[0], z[1]))
        if self.command == "partialintegral":
            for math in self.math_objects:
                if isinstance(math, FunctionManager):
                    calc = Calculus(math)
                    partial_integrals = calc.partial_integrals()
                    for p in partial_integrals:
                        output.append((p[0], p[1]))
        if self.command == "partialderivative":
            for math in self.math_objects:
                if isinstance(math, FunctionManager):
                    calc = Calculus(math)
                    partial_derivatives = calc.partial_derivatives()
                    for p in partial_derivatives:
                        output.append((p[0], p[1]))
        if self.command == "chain":
            for math in self.math_objects:
                if isinstance(math, MarkovChainManager):
                    info, distributions, simulations = math.run_all()
                    output.append((info, distributions, simulations))

        all_errors = all_errors[:-1] if len(all_errors)>1 else ""
        return main_label, output, all_errors

    def process_input(self, command_str):
        """
        (String) -> (String)

        Processes Command arguments into strings based on assumptions made by the interpreter in
        CommandManager

        Output string will be passed the associated DataManager Object
        """
        output_str = command_str.strip()
        output_str = output_str.split("{")
        output_str = output_str[1]

        output_str= output_str[:-1]
        return output_str

    def process_command(self, command_str):
        """
        (String) -> (String)

        Processes command name based on assumptions made by the interpreter in CommandManager
        Output string will be used to run an Algorithm Object"""

        output_str = command_str.strip()
        output_str = output_str.split("{")
        output_str = output_str[0]
        output_str= output_str.strip()
        output_str = output_str.lower()
        if output_str not in self.commands_dict:
            self.ErrorStack.push_error("Command '{}' not recognized  ".format(output_str))
        return output_str if output_str in self.commands_dict else ""

    def process_input_types(self):
        """
        None -> DataManager[]
        Creates a list of input types from the dictionary associating commands to datatypes
        """
        output_list = []
        for i in self.math_types:
            if i == "FunctionManager":
                    output_list.append(FunctionManager(self.arguments))
            if i == "Chain":
                output_list.append(MarkovChainManager(self.arguments))
        return output_list

    def get_interpreted(self):
        output_str = ""
        for m in self.math_objects:
            output_str += m.get_interpreted() + " "
        if self.command == "chain":
            return output_str
        return self.command + "{ " + output_str +"}"

    def get_errors(self):
        output_str = ""
        output_str += self.ErrorStack.get_errors()
        for e in self.math_objects:
            error = e.get_errors()
            if error != "":
                output_str += error + "\n"


        return output_str[:-1].strip() if len(output_str)>1 else "" ##remove the last '\n' character
    # def get_math_interpreted(self):
    #     res = ""
    #     for obj in self.math_objects:
    #         res += obj.get_interpreted()
    #     return res
    #
    # def get_math_uninterpreted(self):
    #     res = ""
    #     for obj in self.math_objects:
    #         res += obj.get_uninterpreted()
    #     return res
    #
    # def get_math_errors(self):
    #     res = ""
    #     for obj in self.math_objects:
    #         res += obj.get_compile_errors()
    #     return res
    #
    # def get_math_object_information(self):
    #     """
    #     None -> (String)
    #
    #     Gets the information produced by the DataManger at dynamic compile time
    #     includes errors/interpreted/uninterpreted
    #     """
    #     res = self.get_math_interpreted()
    #     res += "\n"
    #     res += self.get_math_uninterpreted()
    #     res += self.get_math_errors()
    #     return res

    def get_command_name(self):
        """
        None -> String

        Getter for the command name
        """
        return self.command

if __name__ == "__main__":
    c = Command("partialintegral{f(x,y) = (cos(x+y))}")
    print(c.run())
    # print(c.get_math_object_information())
