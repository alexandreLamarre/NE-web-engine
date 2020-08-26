from src.interpreter import CommandInterpreter
from src.Command import Command
from src.FunctionManager import FunctionManager
from src.Error_Stack import ErrorStack
class CommandManager(CommandInterpreter):
    """ Factory object that processes the command line input
    And instantiates the commands to be run at runtime depending on their specifications

    Implements an Interpreter interface because it processes user input"""

    def __init__(self, commands_str):
        """
        None -> None

        Instantiates a new CommandManager Object

        Interprets the commands as acceptable/unnaceptable using the Interpreter interface
        Creates a list of Command Objects using those strings
        """
        super().__init__()
        self.ErrorStack = ErrorStack()
        self.default = False
        self.original_input = commands_str
        self.command_str_container = self.process_commands(commands_str)
        if not self.default:
            self.uninterpreted = self.process_uninterpreted(commands_str)
            self.Commands_container = [Command(c) for c in self.command_str_container]
            self.commands_queue = list(self.Commands_container)
        else:
            ##TODO update these when we create default command queue, not here
            ## This is a quick fix, do a real fix later
            self.uninterpreted = []
            self.Commands_container = []
    def run_initial(self):
        """
        Gets interpreted commands
        Gets uninterpreted commands
        Gets interpreted input
        Gets uninterpreted input
        Gets errors in input
        """
        if not self.default:
            mainlabel = "Input"
            output = []
            output.append(("Your input: ", self.original_input ))
            output.append(("Interpreted", self.get_interpreted()))
            output.append(("Errors",self.get_errors()))
        else:
            mainlabel = "Input"
            output = []
            temp_function_manager = FunctionManager(self.original_input)
            output.append(("Your input: ", self.original_input ))
            output.append(("Interpreted", temp_function_manager.get_interpreted()))
            output.append(("Errors", temp_function_manager.get_errors() + self.get_errors()))
        return mainlabel, output

    async def run_next(self):
        if len(self.commands_queue) == 0:
            # No label and no [sublabel,info] pairs
            return None,None,None
        next_command = self.commands_queue.pop(0)
        try:
            main_label, sub_labels_and_info,errors = next_command.run()
        except Exception as e:
            main_label,sub_labels_and_info,errors = next_command.command, [], str(e)  # Output is in the form [main label, (sublabel, info), errors]
        return main_label.upper(),sub_labels_and_info,errors

    def process_commands(self, command_string):
        if len(command_string) < 300:
            processed_commands = self.match(command_string)

            if processed_commands != []:
                return processed_commands
            else:
                self.default = True
                self.commands_queue = self.create_default_command_queue()
                return ""
        else:
            self.ErrorStack.push_error("Character limit for input exceeded  ")
            return ""

    def create_default_command_queue(self):
        """
        None -> #TODO

        When no commands are specified in the command line, run default commands.
        """
        #plot, zeroes, derivative, factorization, integral?
        plot = Command("plot{"+self.original_input+"}")
        zeroes = Command("zeroes{" + self.original_input+ "}")
        partial_derivatives = Command("partialderivative{"+self.original_input+"}")
        partial_integral = Command("partialintegral{" + self.original_input+ "}")
        return [zeroes,plot,partial_derivatives,partial_integral]

    def is_default(self):
        return self.default

    def process_uninterpreted(self, in_str):
        """
        (String) -> (String)
        Returns a string representing uninterpreted output
        """
        res = in_str
        for cstr in self.command_str_container:
            assert (cstr in res), "Interpreted input was not even in the input to begin with??"
            start_index = res.find(cstr)
            end_index = start_index + len(cstr)
            res = res[0:start_index] + "\n" + res[end_index:]
            res.strip()
        return res

    def get_interpreted(self):
        """
        (None) -> (String)

        Returns the interpreted commands (matched to regex by interpreter interface) in the command line
        formatted to a user friendly string.
        """
        output_message = ""
        for c in self.Commands_container:
            output_message += c.get_interpreted() + "\n"

        return output_message[:-1] if output_message else ""

    def get_errors(self):
        output_message = ""
        output_message += self.ErrorStack.get_errors()
        for c in self.Commands_container:
            if c.get_errors() != "":
                output_message += c.get_errors() +"\n"

        return output_message[:-1].strip() if len(output_message)>1 else ""## remove last '\n' character

if __name__ == "__main__":

    c = CommandManager("plot{f(x) = sin(x)}")
    print(c.original_input)
    print(c.get_interpreted())


