class ErrorStack:
    """
    Interface for Objects that want to push user-comprehensible
    errors and return them for later use.
    Can also flag to stop the execution of a command, by setting stops

    """
    def __init__(self):
        """ None -> None

        Initializes an Error Stack interface
        By default:
            -Contains no errors
            -The stop flag for stopping execution is set to false
        """
        self.error_str = ""
        self.stop = False

    def push_error(self, error):
        """
        (String) -> None
        """
        self.error_str += error

    def check_errors(self):
        """
        None -> String

        Returns a formatted string that contains errors encoutered by
        whatever class implements this interface.
        """
        return self.error_str

    def set_stop(self):
        """
        None -> None

        Sets the stop flag to true when called. Can be used to stop the program
        after it has encountered many fatal errors, and return all the issues.
        """
        self.stop = True

    def stop_exec(self):
        """ If the stop flag has been called then a fatal error was encountered,
         so we exit the program"""
        if self.stop:
            exit(1)
