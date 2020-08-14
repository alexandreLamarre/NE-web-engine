from src.interpreter import CommandInterpreter
from src.Command import Command


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
        self.done = False
        self.initial_done = False
        self.command_str_container = self.match(commands_str)
        self.uninterpreted = self.process_uninterpreted(commands_str)
        self.Commands_container = [Command(c) for c in self.command_str_container]
        self.commands_queue = list(self.Commands_container)

    def run_initial(self):
        """
        Gets interpreted commands
        Gets uninterpreted commands
        Gets interpreted input
        Gets uninterpreted input
        Gets errors in input
        """
        mainlabel = "Input"
        output = []
        output.append(("Interpreted", self.get_interpreted()))
        output.append(("Uninterpreted",self.get_uninterpreted()))
        output.append(("Errors",self.get_errors()))
        self.initial_done = True
        return mainlabel, output

    def run_next(self):
        if len(self.commands_queue) == 0:
            self.done = True
            # No label and no [sublabel,info] pairs
            return None,None
        next_command = self.commands_queue.pop(0)
        main_label, sub_labels_and_info = next_command.run()
        # Output is in the form [main label, (sublabel, info)]
        return main_label,sub_labels_and_info


    # def run_all(self):
    #     """
    #     None -> #TODO
    #
    #     Runs all commands interpreted by the command manager
    #     """
    #     for c in self.Commands_container:
    #         yield c.run()
    #     self.done = True

    def run_default(self):
        """
        None -> #TODO

        When no commands are specified in the command line, run default commands.
        """
        #plot, zeroes, derivative, factorization, integral?
        pass


    def process_uninterpreted(self, in_str):
        """
        (String) -> (String)

        Processes uninterpreted strings entered in the command line
        by removing the intrepretable input and separating the resulting strings

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
            output_message += "Command" +" '"+c.get_command_name() + "' on: \n" +c.get_math_interpreted()+"\n"

        return output_message if output_message else ""


    def get_uninterpreted(self):
        """
        (None) -> String

        Returns the uninterpreted commands in the command line formatted to a user friendly string
        """
        output_message = self.uninterpreted.strip()
        output_message = "Could not interpret the following as commands :\n" + output_message if output_message else ""
        for c in self.Commands_container:
            unin = c.get_math_uninterpreted()
            if unin:
                output_message += "In " +c.command + " : " + unin +"\n"
        return output_message

    def get_errors(self):
        output_message = ""
        for c in self.Commands_container:
            if c.get_math_errors() != "":
                output_message += "In " + c.command + " : \n" +c.get_math_errors() +"\n"

        return output_message

if __name__ == "__main__":

    c = CommandManager("\plot{f(x) = (x**2)} \plot{laplace(x,y,z) = (x** (1/3), y**(1/3), z**(1/3)) fourrier(x) = (x^5)}")
    print(c.get_interpreted())
    print(c.get_uninterpreted())
    x = 5
    print(x^5)