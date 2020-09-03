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
        self.error_dict = {}

    def push_error(self, error):
        """
        (String) -> None
        """
        if error not in self.error_dict:
            self.error_dict[error] = 1
        else:
            self.error_dict[error] += 1

    def get_errors(self):
        output_str = "<br>"
        for (k,v) in self.error_dict.items():
            if v == 1:
                output_str += k + "<br>"
            else:
                output_str += k + " (" + str(v) + ")" + "<br>"

        return output_str ##remove last '\n'
    # def check_errors(self):
    #     """
    #     None -> String
    #
    #     Returns a formatted string that contains errors encoutered by
    #     whatever class implements this interface.
    #     """
    #     return self.error_str

if __name__ == "__main__":
    e = ErrorStack()
    for i in range(3):
        e.push_error("Function undefined plotting 0 instead")

    print(e.get_errors())

    e.push_error("Function undefined plotting 0 instead")

    print(e.get_errors())
