from src.FunctionManager import FunctionManager
from src.Plot import Plot
from src.Calculus import Calculus
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
        self.arguments = self.process_input(command_str)
        self.command = self.process_command(command_str)


        # 'Static dictionary for the valid input classes inside the command given
        # In the future should be replaced by a database
        self.commands_dict = {'plot': ['FunctionManager'], 'IFS': ['FunctionManager', 'MarkovChain'], \
                              'zeroes' : ['FunctionManager'], 'derivative': ['FunctionManager'], 'integral' : ['FunctionManager'],\
                              'partialderivative' : ['FunctionManager'], 'partialintegral': ['FunctionManager']}
        self.input_types = []

        assert(self.command in self.commands_dict), "Command not recognized"
        self.math_types = self.commands_dict[self.command]
        self.math_objects = self.process_input_types()

    def run(self):
        """
        Runs the command specified on its arguments
        Should return the label of the widget it should be displayed in AND
        Should return the tuple (sublabels, info) that should be displayed in label should be displayed in
        """
        output = []
        main_label = self.command
        if self.command == 'plot':
            for math in self.math_objects:
                if isinstance(math,FunctionManager):
                    plot = Plot(math)
                    figures = plot.run()
                    for f in figures:
                        output.append((None, f))
        if self.command == "zeroes":
            for math in self.math_objects:
                if isinstance(math, FunctionManager):
                    calc = Calculus(math)
                    zeroes = calc.zeroes()
                    for z in zeroes:
                        output.append((z[0], z[1]))
        return main_label, output

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

        return output_str

    def process_input_types(self):
        """
        None -> DataManager[]
        Creates a list of input types from the dictionary associating commands to datatypes
        """
        output_list = []
        for i in self.math_types:
            if i == "FunctionManager":
                    output_list.append(FunctionManager(self.arguments))
        return output_list

    def get_math_interpreted(self):
        res = ""
        for obj in self.math_objects:
            res += obj.get_interpreted()
        return res

    def get_math_uninterpreted(self):
        res = ""
        for obj in self.math_objects:
            res += obj.get_uninterpreted()
        return res

    def get_math_errors(self):
        res = ""
        for obj in self.math_objects:
            res += obj.get_compile_errors()
        return res

    def get_math_object_information(self):
        """
        None -> (String)

        Gets the information produced by the DataManger at dynamic compile time
        includes errors/interpreted/uninterpreted
        """
        res = self.get_math_interpreted()
        res += "\n"
        res += self.get_math_uninterpreted()
        res += self.get_math_errors()
        return res

    def get_command_name(self):
        """
        None -> String

        Getter for the command name
        """
        return self.command

if __name__ == "__main__":
    c = Command("\plot{f(x) = (x**2), g(x) = (x**2) h(x = (a+bc)}")
    print(c.get_math_object_information())