from src.interpreter import Interpreter

class DataManager(Interpreter):
    """
    Abstract Super class that manages a factory of 'Data'-specific objects
    """
    def __init(self):
        pass

    def get_interpreted(self):
        pass

    def get_errors(self):
        pass

    def get_uninterpreted(self, in_str):
        pass

    def process_uninterpreted(self, uninterpreted_string):
        pass

    def generate_reason_uninterpreted(self, unintepreted_string):
        pass